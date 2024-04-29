import pydeck as pdk

DATA_URL = "boston_taxval.geojson"
LAND_COVER = [[[-71.190905, 42.227920], [-71.190905, 42.396986], [-70.868654, 42.396986], [-71.190905, 42.396986]]]

INITIAL_VIEW_STATE = pdk.ViewState(latitude=42.3, longitude=-71.1, zoom=11, max_zoom=18, pitch=45, bearing=0)

polygon = pdk.Layer(
    "PolygonLayer",
    LAND_COVER,
    stroked=False,
    # processes the data as a flat longitude-latitude pair
    get_polygon="-",
    get_fill_color=[0, 0, 0, 20],
)

geojson = pdk.Layer(
    "GeoJsonLayer",
    DATA_URL,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.value_acre / 200000",
    get_fill_color="""
        properties.value_acre < 500000 ? [50, 50, 50, 255] :
        properties.value_acre < 1000000 ? [45,103,63	, 255] :
        properties.value_acre < 3000000 ? [72,	149,	92	, 255] :
        properties.value_acre < 5000000 ? [176,214,125	, 255] :
        properties.value_acre < 6000000 ? [255,253,192	, 255] :
        properties.value_acre < 7500000 ? [249,225,153	, 255] :
        properties.value_acre < 10000000 ? [242,177,113	, 255] :
        properties.value_acre < 20000000 ? [232, 117, 77	, 255] :
        properties.value_acre < 50000000 ? [201, 62, 53, 255] :
        properties.value_acre < 150000000 ? [150, 30 47, 255] :
        [154, 30, 220, 255] 
    """,
    get_line_color=[255, 255, 255],
)

r = pdk.Deck(layers=[geojson], initial_view_state=INITIAL_VIEW_STATE)

r.to_html("geojson_layer.html")
