import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from features import extract_features


print("Loading data...")
try:
    df1 = pd.read_csv("phishing.csv")   # phishing URLs
    df2 = pd.read_csv("benign.csv")     # legitimate URLs
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()


if 'label' not in df1.columns:
    df1['label'] = 1
else:
    df1['label'] = 1

if 'label' not in df2.columns:
    df2['label'] = 0
else:
    df2['label'] = 0

df = pd.concat([df1, df2], ignore_index=True)


def force_int_label(val):
    if str(val).lower() in ['phishing', '1', '1.0', 'bad']:
        return 1
    return 0

df['label'] = df['label'].apply(force_int_label)

df['label'] = df['label'].astype(int)

print(f"Total samples: {len(df)}")
print("Class Distribution:\n", df['label'].value_counts())

df = df.dropna(subset=['url', 'label'])
df = df.drop_duplicates(subset=['url'])
df['label'] = df['label'].astype(int)

print(f"Total samples: {len(df)}")
print("Class Distribution:\n", df['label'].value_counts(normalize=True))


print("\nExtracting features... (This may take a while depending on dataset size)")
X = list(df['url'].apply(extract_features))
y = df['label'].tolist()


X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y
)


print("Training Random Forest Model...")

model = RandomForestClassifier(
    n_estimators=200,      # More trees for better stability
    max_depth=25,          # Prevents extreme overfitting while allowing complexity
    min_samples_split=5, 
    class_weight='balanced', # CRITICAL: Handles data imbalance automatically
    random_state=42,
    n_jobs=-1              # Use all CPU cores
)

model.fit(X_train, y_train)


print("\n--- Evaluation Results ---")
y_pred = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nDetailed Report:")
print(classification_report(y_test, y_pred, target_names=['Legitimate', 'Phishing']))


joblib.dump(model, "model.pkl")
print("\nSuccess: model.pkl has been saved.")