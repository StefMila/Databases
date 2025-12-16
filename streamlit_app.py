import streamlit as st
from sqlalchemy import text

def show_view_data():
    """Display all data with queries"""
    conn = st.connection("postgresql", type="sql")
    st.header('📊 View Database')
    
    # Select view type
    view_type = st.selectbox("Select what to view", 
                             ["All Paintings", "All Artists", "All Cities", 
                              "Paintings by City", "Paintings by Artist", "Paintings by Style"])
    
    if view_type == "All Paintings":
        st.subheader("All Paintings")
        query = """
            SELECT 
                p.serial_number,
                p.title,
                p.style_type,
                p.year_created,
                a.first_name || ' ' || a.last_name AS artist_name,
                c.name AS city_name,
                co.country_name,
                p.wikipedia_url
            FROM painting p
            JOIN painted pt ON p.serial_number = pt.painting_serial_number
            JOIN artist a ON pt.artist_id = a.id
            JOIN visitable v ON p.serial_number = v.painting_serial_number
            JOIN city c ON v.city_country_iso = c.country_iso AND v.city_zipcode = c.zipcode
            JOIN country co ON c.country_iso = co.iso
            ORDER BY p.serial_number;
        """
        df = conn.query(query, ttl=0)
        
        # Create clickable links for Wikipedia
        if 'wikipedia_url' in df.columns:
            df['wikipedia'] = df['wikipedia_url'].apply(
                lambda x: f'<a href="{x}" target="_blank">Wikipedia</a>' if x else ''
            )
            df = df.drop('wikipedia_url', axis=1)
        
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        st.metric("Total Paintings", len(df))
    
    elif view_type == "All Artists":
        st.subheader("All Artists")
        query = """
            SELECT 
                a.id,
                a.first_name,
                a.last_name,
                a.birth_year,
                a.death_year,
                COUNT(pt.painting_serial_number) AS number_of_paintings
            FROM artist a
            LEFT JOIN painted pt ON a.id = pt.artist_id
            GROUP BY a.id, a.first_name, a.last_name, a.birth_year, a.death_year
            ORDER BY a.last_name, a.first_name;
        """
        df = conn.query(query, ttl=0)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Artists", len(df))
    
    elif view_type == "All Cities":
        st.subheader("All Cities")
        query = """
            SELECT 
                c.country_iso,
                c.zipcode,
                c.name,
                co.country_name,
                COUNT(v.painting_serial_number) AS paintings_count
            FROM city c
            JOIN country co ON c.country_iso = co.iso
            LEFT JOIN visitable v ON c.country_iso = v.city_country_iso AND c.zipcode = v.city_zipcode
            GROUP BY c.country_iso, c.zipcode, c.name, co.country_name
            ORDER BY paintings_count DESC, c.name;
        """
        df = conn.query(query, ttl=0)
        st.dataframe(df, use_container_width=True)
        st.metric("Total Cities", len(df))
    
    elif view_type == "Paintings by City":
        st.subheader("Paintings by City")
        cities_df = conn.query("SELECT country_iso, zipcode, name FROM city ORDER BY name;", ttl=0)
        city_options = {f"{row['name']} ({row['zipcode']})": (row['country_iso'], row['zipcode']) 
                       for _, row in cities_df.iterrows()}
        
        selected_city = st.selectbox("Select City", list(city_options.keys()))
        
        if selected_city:
            country_iso, zipcode = city_options[selected_city]
            query = """
                SELECT 
                    p.title,
                    p.style_type,
                    p.year_created,
                    a.first_name || ' ' || a.last_name AS artist_name
                FROM painting p
                JOIN visitable v ON p.serial_number = v.painting_serial_number
                JOIN painted pt ON p.serial_number = pt.painting_serial_number
                JOIN artist a ON pt.artist_id = a.id
                WHERE v.city_country_iso = :country_iso AND v.city_zipcode = :zipcode
                ORDER BY p.year_created;
            """
            df = conn.query(query, params={"country_iso": country_iso, "zipcode": zipcode}, ttl=0)
            st.dataframe(df, use_container_width=True)
            st.metric("Paintings in this city", len(df))
    
    elif view_type == "Paintings by Artist":
        st.subheader("Paintings by Artist")
        artists_df = conn.query(
            "SELECT id, first_name, last_name FROM artist ORDER BY last_name, first_name;", 
            ttl=0)
        artist_options = {f"{row['first_name']} {row['last_name']}": row['id'] 
                         for _, row in artists_df.iterrows()}
        
        selected_artist = st.selectbox("Select Artist", list(artist_options.keys()))
        
        if selected_artist:
            artist_id = artist_options[selected_artist]
            query = """
                SELECT 
                    p.title,
                    p.style_type,
                    p.year_created,
                    c.name AS city_name,
                    co.country_name
                FROM painting p
                JOIN painted pt ON p.serial_number = pt.painting_serial_number
                JOIN visitable v ON p.serial_number = v.painting_serial_number
                JOIN city c ON v.city_country_iso = c.country_iso AND v.city_zipcode = c.zipcode
                JOIN country co ON c.country_iso = co.iso
                WHERE pt.artist_id = :artist_id
                ORDER BY p.year_created;
            """
            df = conn.query(query, params={"artist_id": artist_id}, ttl=0)
            st.dataframe(df, use_container_width=True)
            st.metric("Paintings by this artist", len(df))
    
    elif view_type == "Paintings by Style":
        st.subheader("Paintings by Style")
        styles_df = conn.query("SELECT DISTINCT style_type FROM painting ORDER BY style_type;", ttl=0)
        
        selected_style = st.selectbox("Select Style", styles_df['style_type'].tolist())
        
        if selected_style:
            query = """
                SELECT 
                    p.title,
                    p.year_created,
                    a.first_name || ' ' || a.last_name AS artist_name,
                    c.name AS city_name
                FROM painting p
                JOIN painted pt ON p.serial_number = pt.painting_serial_number
                JOIN artist a ON pt.artist_id = a.id
                JOIN visitable v ON p.serial_number = v.painting_serial_number
                JOIN city c ON v.city_country_iso = c.country_iso AND v.city_zipcode = c.zipcode
                WHERE p.style_type = :style
                ORDER BY p.year_created;
            """
            df = conn.query(query, params={"style": selected_style}, ttl=0)
            st.dataframe(df, use_container_width=True)
            st.metric("Paintings in this style", len(df))

def show_advanced_search():
    """Advanced search with multi-select filters"""
    conn = st.connection("postgresql", type="sql")
    st.header('🔍 Advanced Search')
    st.write("Use multiple filters to find specific paintings")
    
    # Get all filter options
    countries_df = conn.query("SELECT DISTINCT iso, country_name FROM country ORDER BY country_name;", ttl=0)
    cities_df = conn.query("SELECT DISTINCT zipcode, name FROM city ORDER BY name;", ttl=0)
    artists_df = conn.query("SELECT DISTINCT id, first_name, last_name FROM artist ORDER BY last_name, first_name;", ttl=0)
    styles_df = conn.query("SELECT DISTINCT style_type FROM painting ORDER BY style_type;", ttl=0)
    
    # Create filter options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Geographic Filters")
        selected_countries = st.multiselect(
            "Select Countries",
            options=countries_df['country_name'].tolist(),
            default=None
        )
        
        selected_cities = st.multiselect(
            "Select Cities",
            options=cities_df['name'].tolist(),
            default=None
        )
    
    with col2:
        st.subheader("Art Filters")
        selected_artists = st.multiselect(
            "Select Artists",
            options=[f"{row['first_name']} {row['last_name']}" for _, row in artists_df.iterrows()],
            default=None
        )
        
        selected_styles = st.multiselect(
            "Select Painting Styles",
            options=styles_df['style_type'].tolist(),
            default=None
        )
    
    # Build dynamic query based on filters
    query = """
        SELECT 
            p.serial_number,
            p.title,
            p.style_type,
            p.year_created,
            a.first_name || ' ' || a.last_name AS artist_name,
            c.name AS city_name,
            co.country_name,
            p.wikipedia_url
        FROM painting p
        JOIN painted pt ON p.serial_number = pt.painting_serial_number
        JOIN artist a ON pt.artist_id = a.id
        JOIN visitable v ON p.serial_number = v.painting_serial_number
        JOIN city c ON v.city_country_iso = c.country_iso AND v.city_zipcode = c.zipcode
        JOIN country co ON c.country_iso = co.iso
        WHERE 1=1
    """
    
    params = {}
    
    # Add filters dynamically
    if selected_countries:
        query += " AND co.country_name = ANY(:countries)"
        params['countries'] = selected_countries
    
    if selected_cities:
        query += " AND c.name = ANY(:cities)"
        params['cities'] = selected_cities
    
    if selected_artists:
        # Convert artist names back to format for comparison
        query += " AND (a.first_name || ' ' || a.last_name) = ANY(:artists)"
        params['artists'] = selected_artists
    
    if selected_styles:
        query += " AND p.style_type = ANY(:styles)"
        params['styles'] = selected_styles
    
    query += " ORDER BY p.year_created, p.title;"
    
    # Execute query
    if params:
        df = conn.query(query, params=params, ttl=0)
    else:
        df = conn.query(query, ttl=0)
    
    # Display results
    st.subheader(f"Search Results ({len(df)} paintings found)")
    
    if len(df) > 0:
        # Create clickable links for Wikipedia
        if 'wikipedia_url' in df.columns:
            df['wikipedia'] = df['wikipedia_url'].apply(
                lambda x: f'<a href="{x}" target="_blank">🔗 View</a>' if x else ''
            )
            df = df.drop('wikipedia_url', axis=1)
        
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        
        # Show summary statistics
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Paintings", len(df))
        with col2:
            st.metric("Different Artists", df['artist_name'].nunique())
        with col3:
            st.metric("Different Styles", df['style_type'].nunique())
    else:
        st.info("No paintings found with the selected filters. Try adjusting your selection.")

def show_add_artist():
    """Form to add a new artist"""
    conn = st.connection("postgresql", type="sql")
    st.header('➕ Add New Artist')
    
    with st.form("add_artist_form"):
        first_name = st.text_input("First Name*")
        last_name = st.text_input("Last Name*")
        birth_year = st.number_input("Birth Year", min_value=1000, max_value=2024, 
                                     value=1900, step=1)
        death_year = st.number_input("Death Year (leave as 0 if alive)", 
                                     min_value=0, max_value=2024, value=0, step=1)
        
        submitted = st.form_submit_button("Add Artist")
        
        if submitted:
            if first_name and last_name:
                try:
                    with conn.session as s:
                        if death_year == 0:
                            s.execute(
                                text("""
                                    INSERT INTO artist (first_name, last_name, birth_year, death_year)
                                    VALUES (:fn, :ln, :by, NULL)
                                """),
                                {"fn": first_name, "ln": last_name, "by": birth_year}
                            )
                        else:
                            s.execute(
                                text("""
                                    INSERT INTO artist (first_name, last_name, birth_year, death_year)
                                    VALUES (:fn, :ln, :by, :dy)
                                """),
                                {"fn": first_name, "ln": last_name, "by": birth_year, "dy": death_year}
                            )
                        s.commit()
                    st.success(f"✅ Successfully added artist: {first_name} {last_name}")
                except Exception as e:
                    st.error(f"❌ Error adding artist: {e}")
            else:
                st.error("❌ Please fill in all required fields (marked with *)")

def show_add_city():
    """Form to add a new city"""
    conn = st.connection("postgresql", type="sql")
    st.header('➕ Add New City')
    
    # Get countries for dropdown
    countries_df = conn.query("SELECT iso, country_name FROM country ORDER BY country_name;", ttl=0)
    country_options = {f"{row['country_name']} ({row['iso']})": row['iso'] 
                      for _, row in countries_df.iterrows()}
    
    with st.form("add_city_form"):
        country = st.selectbox("Country*", list(country_options.keys()))
        zipcode = st.text_input("Zipcode*")
        name = st.text_input("City Name*")
        
        submitted = st.form_submit_button("Add City")
        
        if submitted:
            if zipcode and name and country:
                try:
                    country_iso = country_options[country]
                    with conn.session as s:
                        s.execute(
                            text("""
                                INSERT INTO city (country_iso, zipcode, name)
                                VALUES (:ci, :zc, :n)
                            """),
                            {"ci": country_iso, "zc": zipcode, "n": name}
                        )
                        s.commit()
                    st.success(f"✅ Successfully added city: {name}")
                except Exception as e:
                    st.error(f"❌ Error adding city: {e}")
            else:
                st.error("❌ Please fill in all required fields (marked with *)")

def show_add_painting():
    """Form to add a new painting"""
    conn = st.connection("postgresql", type="sql")
    st.header('➕ Add New Painting')
    
    # Predefined list of painting styles
    painting_styles = [
        'Renaissance',
        'Baroque',
        'Rococo',
        'Neoclassicism',
        'Romanticism',
        'Realism',
        'Impressionism',
        'Post-Impressionism',
        'Expressionism',
        'Cubism',
        'Futurism',
        'Surrealism',
        'Abstract Expressionism',
        'Pop Art',
        'Minimalism',
        'Contemporary'
    ]
    
    # Get artists and cities for dropdowns
    artists_df = conn.query(
        "SELECT id, first_name, last_name FROM artist ORDER BY last_name, first_name;", 
        ttl=0)
    artist_options = {f"{row['first_name']} {row['last_name']}": row['id'] 
                     for _, row in artists_df.iterrows()}
    
    cities_df = conn.query("SELECT country_iso, zipcode, name FROM city ORDER BY name;", ttl=0)
    city_options = {f"{row['name']} ({row['zipcode']})": (row['country_iso'], row['zipcode']) 
                   for _, row in cities_df.iterrows()}
    
    with st.form("add_painting_form"):
        title = st.text_input("Painting Title*")
        style_type = st.selectbox("Style Type*", painting_styles)
        year_created = st.number_input("Year Created", min_value=1000, max_value=2024, 
                                       value=2000, step=1)
        wikipedia_url = st.text_input("Wikipedia URL (optional)")
        artist = st.selectbox("Artist*", list(artist_options.keys()))
        city = st.selectbox("City (where painting is located)*", list(city_options.keys()))
        
        submitted = st.form_submit_button("Add Painting")
        
        if submitted:
            if title and style_type and artist and city:
                try:
                    artist_id = artist_options[artist]
                    city_country_iso, city_zipcode = city_options[city]
                    
                    with conn.session as s:
                        # Insert painting first
                        if wikipedia_url:
                            result = s.execute(
                                text("""
                                    INSERT INTO painting (title, style_type, year_created, wikipedia_url)
                                    VALUES (:t, :st, :yc, :wiki)
                                    RETURNING serial_number
                                """),
                                {"t": title, "st": style_type, "yc": year_created, "wiki": wikipedia_url}
                            )
                        else:
                            result = s.execute(
                                text("""
                                    INSERT INTO painting (title, style_type, year_created)
                                    VALUES (:t, :st, :yc)
                                    RETURNING serial_number
                                """),
                                {"t": title, "st": style_type, "yc": year_created}
                            )
                        
                        painting_id = result.fetchone()[0]
                        
                        # Insert into painted relationship
                        s.execute(
                            text("""
                                INSERT INTO painted (artist_id, painting_serial_number)
                                VALUES (:aid, :psn)
                            """),
                            {"aid": artist_id, "psn": painting_id}
                        )
                        
                        # Insert into visitable relationship
                        s.execute(
                            text("""
                                INSERT INTO visitable (city_country_iso, city_zipcode, painting_serial_number)
                                VALUES (:cciso, :czc, :psn)
                            """),
                            {"cciso": city_country_iso, "czc": city_zipcode, "psn": painting_id}
                        )
                        
                        s.commit()
                    st.success(f"✅ Successfully added painting: {title}")
                except Exception as e:
                    st.error(f"❌ Error adding painting: {e}")
            else:
                st.error("❌ Please fill in all required fields (marked with *)")

# Configure pages
pg = st.navigation([
    st.Page(show_view_data, title="View Data", icon="📊"),
    st.Page(show_advanced_search, title="Advanced Search", icon="🔍"),
    st.Page(show_add_artist, title="Add Artist", icon="➕"),
    st.Page(show_add_city, title="Add City", icon="🏙️"),
    st.Page(show_add_painting, title="Add Painting", icon="🎨"),
])

st.set_page_config(page_title="Painters & Paintings", page_icon="🎨")
st.title('🎨 Painters & Paintings Management System')

if __name__ == "__main__":
    pg.run()
