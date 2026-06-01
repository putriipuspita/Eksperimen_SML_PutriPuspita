import pandas as pd

def preprocess_data():

    # Load Dataset
    df_customer_churn = pd.read_csv("../customer_churn_raw/customer_churn.csv")

    # TotalCharges ke numerik
    df_customer_churn["TotalCharges"] = pd.to_numeric(
        df_customer_churn["TotalCharges"],
        errors="coerce"
    )

    # Missing Value
    df_customer_churn["TotalCharges"] = df_customer_churn["TotalCharges"].fillna(
        df_customer_churn["TotalCharges"].median()
    )

    # Hapus customerID
    df_customer_churn.drop(
        columns=["customerID"],
        inplace=True
    )

    # Encoding
    # Mengubah Kolom Churn
    df_customer_churn['Churn'] = df_customer_churn['Churn'].map({
    'Yes' : 1,
    'No' : 0
    })

    kolom_kategori = df_customer_churn.select_dtypes('object').columns

    # Memisahkan Kolom 2 kategori dan 3 Kategori
    kolom_2_kategori = []
    kolom_multikategori = []

    for kolom in kolom_kategori : 
        if df_customer_churn[kolom].nunique() == 2 : 
            kolom_2_kategori.append(kolom)
        else : 
            kolom_multikategori.append(kolom)

    # Encoding Kolom 2 Kategori
    for kolom in kolom_2_kategori : 
        nilai_unik = sorted(df_customer_churn[kolom].unique())

        # Mappping
        mapping = {
            nilai_unik[0]: 0,
            nilai_unik[1]: 1
        }

        df_customer_churn[kolom] = df_customer_churn[kolom].map(mapping)

    # Encoding Kolom Multikategori
    df_customer_churn = pd.get_dummies(df_customer_churn, columns=kolom_multikategori, drop_first=True)


    # Simpan
    df_customer_churn.to_csv(
        "customer_churn_preprocessing.csv",
        index=False
    )

    print("Preprocessing selesai")

if __name__ == "__main__":
    preprocess_data()