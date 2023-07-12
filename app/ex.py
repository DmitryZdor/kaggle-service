import pandas as pd



with open("../data/train_test_split.csv", "r", encoding="utf-8") as csv_f:
    df = pd.read_csv(csv_f)
    # res = df.filter(["title", "views_on_vd"])[:10]
    # res = df.sort_values(["views_on_vd"], ascending=False).filter(items=["title", "views_on_vd"])[:10]
    print(df.to_dict(index=True, orient="records"))