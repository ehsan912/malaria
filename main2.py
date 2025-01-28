import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("PROJECT MALARIA")

st.image(
    "https://www.news-medical.net/image.axd?picture=2018/5/shutterstock_KATERYNA_KON-2.jpg",
    caption="Mosquito"
)

st.write("""
Sickle cell disease is a group of inherited blood disorders that causes the red blood cells (RBCs) to have abnormal hemoglobin, called hemoglobin S. People with the disease have RBCs which are crescent-shaped, sticky, and rigid. The affected individual is likely to have blocked blood vessels and a variety of other problems ranging from pain to infections.

Sickle cell trait is a genetic condition that refers to the individual inheriting both the sickle cell gene (hemoglobin S) and the normal hemoglobin gene (hemoglobin A). Individuals with sickle cell trait do not show any symptoms compared to those with sickle cell disease. Moreover, they show partial resistance to malaria as malarial parasites (*Plasmodium*) find it harder to grow inside their RBCs.
""")

st.title("HOW IT WORKS")

st.write("""
You will input the initial allele frequencies, malaria prevalence, and the number of generations.
The simulation will run and visualize how the frequencies of allele A and S evolve based on heterozygote advantage and fitness values affected by malaria.
""")

# Simulation Function
def genetics_simulation(initial_A, initial_S, malaria_prevalence, number_of_generations):
    malaria_prevalence /= 100.0  # Convert percentage to proportion
    AA_fitness = 1 - malaria_prevalence
    AS_fitness = 1.0
    SS_fitness = 0.2

    frequency_A = initial_A
    frequency_S = initial_S
    frequency_A_till_end = [frequency_A]
    frequency_S_till_end = [frequency_S]

    for _ in range(int(number_of_generations)):
        AA = frequency_A ** 2
        AS = 2 * frequency_A * frequency_S  # Hardy–Weinberg principle
        SS = frequency_S ** 2

        # Mean fitness
        mean_fitness = (AA * AA_fitness) + (AS * AS_fitness) + (SS * SS_fitness)
            
        # Update allele frequencies
        frequency_A = ((AA * AA_fitness) + (0.5 * AS * AS_fitness)) / mean_fitness
        frequency_S = ((SS * SS_fitness) + (0.5 * AS * AS_fitness)) / mean_fitness

        # Store frequencies
        frequency_A_till_end.append(frequency_A)
        frequency_S_till_end.append(frequency_S)

    return frequency_A_till_end, frequency_S_till_end

# Streamlit App
def main():
    st.title("Sickle Cell and Malaria Simulation")

    # Input options
    initial_A = st.slider('Initial frequency of allele A', 0.0, 1.0, 0.6)
    initial_S = st.slider('Initial frequency of allele S', 0.0, 1.0, 0.4)

    if abs((initial_A + initial_S) - 1.0) > 0.01:
        st.error("Initial frequencies of A and S must sum to 1.0")
        return  # Stop the app if the sum is not approximately 1.0

    malaria_prevalence = st.slider("Malaria Prevalence Rate (%)", 0, 100, 70)
    number_of_generations = st.number_input(
        "Number of generations to simulate", min_value=1, max_value=1000, value=100
    )

    if st.button("Run Simulation"):
        frequency_A_till_end, frequency_S_till_end = genetics_simulation(
            initial_A, initial_S, malaria_prevalence, number_of_generations
        )

        # Visualization using Line Chart
        st.write("### Allele Frequency Trends Over Generations")
        data = {
            'Generations': range(int(number_of_generations) + 1),
            'Allele A': frequency_A_till_end,
            'Allele S': frequency_S_till_end
        }
        df = pd.DataFrame(data)
        df = df.set_index('Generations')
        st.line_chart(df)

        # Results
        st.subheader("Final Allele Frequencies")
        st.write(f"Allele A: {frequency_A_till_end[-1]:.3f}")
        st.write(f"Allele S: {frequency_S_till_end[-1]:.3f}")

if __name__ == "__main__":
    main()

def add_bg_from_url(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{url}");
            background-size: cover;
            opacity: 1.0; /* Adjust the opacity as needed */
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_url('https://wallpaperaccess.com/full/10900224.png')

st.write("""
**Heterozygote Advantage**

Heterozygote advantage refers to a situation where individuals who are heterozygous (having two different alleles) for a particular gene have a higher fitness than those who are homozygous (having two copies of the same allele). In the case of sickle cell disease, individuals with one sickle cell allele (HbS) and one normal allele (HbA) have increased resistance to malaria compared to those with two normal alleles (HbAA).

Malaria is caused by the *Plasmodium* parasite, which infects red blood cells. The sickle cell trait (HbAS) provides a survival advantage in malaria-endemic regions because the altered shape of the sickle-shaped red blood cells makes it harder for the parasite to infect and survive. As a result, individuals with the sickle cell trait are less likely to suffer severe malaria.

In regions with high malaria prevalence, the sickle cell allele (HbS) is maintained in the population because heterozygotes (HbAS) have a survival advantage. This selective pressure increases the frequency of the HbS allele in these regions. However, individuals who are homozygous for the sickle cell allele (HbSS) suffer from sickle cell disease, which can be debilitating and even life-threatening. Therefore, the HbA allele is also maintained in the population to prevent the high prevalence of sickle cell disease.

The heterozygote advantage helps maintain genetic diversity within the population. By providing a survival advantage to heterozygotes, it ensures that both the HbA and HbS alleles persist in the gene pool. This genetic diversity is beneficial for the population's adaptability to changing environments and resistance to diseases.
""")