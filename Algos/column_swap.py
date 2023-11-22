import pandas as pd

df = pd.DataFrame(
    {
        "a": ["something", "", "some other thing", "<null>"],
        "b": ["bla", "blah", "whatever", "val"]
    }
)

for i in df.index:
    # filter on whatever the values for "empty" are here.
    # I think you said it was something like "" and [NULL] for
    # the empty values
    if df.loc[i, "a"] != "" and df.loc[i, "a"] != "<null>":
        val = df.loc[i, "a"]
    else:
        val = df.loc[i, "b"]
    df.loc[i, "a"] = val

df.drop("b", axis=1, inplace=True)

print(df)
