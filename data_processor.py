import pandas as pd


# removes specified keywords from data, returns altered df
def remove_keywords(
    remove_ls,
    import_path='datasets/republican_comments.csv'
):
    df = pd.read_csv(import_path)
    comments_df = df[["comment"]]

    # removes rows from the dataframe which contain keywords in remove_ls
    print("BEFORE:", comments_df)
    print(type(comments_df.comment))
    for keyword in remove_ls:
        comments_df = comments_df[comments_df["comment"].str.contains(keyword)==False]
    print("AFTER:", comments_df)
    return comments_df


remove_keywords(['Trump', 'Biden'])
