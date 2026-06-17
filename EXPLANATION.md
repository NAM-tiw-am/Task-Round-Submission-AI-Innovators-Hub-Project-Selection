# EXPLANATION.md

---

## Questions for Everyone

### 1. What percentage of customers in your dataset have `y = yes`? What does this imbalance mean for how you'd evaluate a model?

Out of 45,211 customers, 5,289 subscribed — that's **11.70%**. The remaining 88.30% did not subscribe. This heavy imbalance means a model that just predicts "no" for every customer would hit ~88% accuracy while being completely useless. Accuracy alone is therefore a misleading metric here — you need precision, recall, and F1 to understand how well the model actually catches the minority class.

---

### 2. Which job category had the highest subscription rate? Does this make sense to you intuitively?

**Students** had the highest subscription rate at **28.68%**, followed by retired customers at 22.79%. This makes intuitive sense — students are likely opening their first financial products, are more open to guidance from bank representatives, and have fewer existing financial commitments competing for their attention. Retired customers likely have accumulated savings and are actively looking for safe, fixed-return products like term deposits.

---

## Track B — ML Engineer (Additional Questions)

### 3. Which feature had the highest importance in your tree-based model? Why do you think that is?

**`duration`** — the length of the last phone call — had by far the highest importance at **34.47%**, more than double the next feature (`month` at 14.66%). This makes sense: if a customer stayed on the call long enough to discuss the product in depth, they were likely already engaged or interested. A very short call almost always ended in a "no." However, this feature has a practical problem — you only know `duration` after the call ends, so it can't realistically be used to target customers beforehand.

---

### 4. Why is F1 a better metric than accuracy for this particular dataset?

With only 11.70% of customers subscribing, the classes are severely imbalanced. A model predicting "no" for everyone would score ~88% accuracy but have 0% recall for the class that actually matters. F1 balances precision (how many predicted "yes" were actually "yes") and recall (how many actual "yes" customers were caught), giving a single score that penalises the model for ignoring the minority class. For a bank trying to identify likely subscribers, missing real prospects (low recall) is just as costly as calling the wrong people (low precision).

---

### 5. Pick one of your 5 sample predictions. Do you actually agree with the model's call?

**Customer #30441** — 55-year-old married blue-collar worker, secondary education, balance of €1,765, housing loan active, contacted by phone in February, call lasted 445 seconds, previous campaign outcome was a **failure**.

The model predicted **"no"** with 55.41% probability — essentially a coin flip. I partially agree with the call, but I'd flag this one as genuinely borderline. The long call duration (445s) and the fact he was contacted again after a prior failed campaign suggest some residual interest. On the other hand, blue-collar workers have the lowest overall subscription rate (7.27%) in this dataset, he carries a housing loan, and his last campaign outcome was explicitly "failure" — all signals pointing away from a subscription. The model's low confidence here reflects the real ambiguity in this customer's profile.

---
