# Reflection: Using GitHub Copilot for Data Cleaning

## What Copilot Generated

I used GitHub Copilot to help draft the `load_data` and `clean_column_names` functions. To trigger Copilot, I wrote a detailed comment above each function describing exactly what it should do — for example, "reads a CSV file from the given path and returns it as a DataFrame." Copilot then suggested the full function body. For `load_data`, it produced a standard `pd.read_csv` call and a return statement. For `clean_column_names`, it suggested chaining `.str.strip()` and `.str.lower()` on `df.columns`, which was a clean approach I hadn't initially planned to chain in one expression.

## What I Modified

Copilot's first suggestion for `clean_column_names` only did `.str.lower()` and `.str.strip()` but didn't replace spaces inside column names with underscores. I added `.str.replace(" ", "_")` because column names like `date sold` would require bracket notation throughout the rest of the code instead of dot notation. I also modified the `handle_missing_values` function significantly. Copilot suggested dropping all rows with *any* missing value, which would have deleted too much useful data. Instead, I changed the logic to only drop rows where *both* price and quantity are missing, and fill the remaining gaps with the median price and a quantity of 1. This preserved more rows while still being defensible. I also renamed Copilot's generic variable `data` to `df` throughout to match standard pandas convention.

## What I Learned

This project taught me that data cleaning is less about writing complicated code and more about making consistent decisions. For example, deciding *why* to fill a missing quantity with 1 (rather than dropping the row or using the mean) forced me to think about what the data actually represents. I also learned that Copilot is most useful when you give it very specific comments — vague comments produce vague code. The clearest example was when I wrote "Converts all column headers to lowercase with underscores and removes surrounding whitespace" and Copilot produced much more useful code than when I had first tried a one-line comment like "clean column names." One limitation I noticed is that Copilot does not understand your specific dataset; it generated generic logic that I had to adapt once I actually looked at the raw CSV and saw problems like negative prices and extra whitespace inside product names. The tool speeds up boilerplate but still requires the programmer to understand the data and make judgment calls.
