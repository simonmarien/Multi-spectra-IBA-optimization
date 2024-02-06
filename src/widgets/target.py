import streamlit as st


# Function to display the dictionary
def display_target(target):
    # Display the target dictionary

    for index, layer in enumerate(target['layerList']):
        st.markdown("### Layer " + str(index + 1))
        st.table({"Areal density": [layer['arealDensity']], "Minimum areal density": [layer['min_AD']], "Maximum areal density": [layer['max_AD']], "Mass density": [layer['massDensity']], "Thickness": [layer['thickness']]})
        st.write("#### Elements:")
        for element in layer['elementList']:
            st.write("##### Element " + str(element['atomicNumber']))
            st.table({"Areal density": [element['arealDensity']], "Ratio": [element['ratio']], "Minimum ratio": [element['min_ratio']], "Maximum ratio": [element['max_ratio']]})
            st.write("###### Isotopes:")
            st.table(element['isotopeList'])
