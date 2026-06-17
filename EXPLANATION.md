# EXPLANATION.md

---

## Questions for Everyone

### 1. What percentage of customers in your dataset have `y = yes`? What does this imbalance mean for how you'd evaluate a model?

Out of 45,211 customers, 5,289 subscribed — that's **11.70%**. The remaining 88.30% did not subscribe. This heavy imbalance means a model that just predicts no for every customer would hit 88% accuracy while being completely useless. Accuracy alone is therefore a misleading metric here — you need precision, recall, and F1 to understand how well the model actually catches the minority class.

---

### 2. Which job category had the highest subscription rate? Does this make sense to you intuitively?

**Students** had the highest subscription rate at **28.68%**, followed by retired customers at 22.79%.
At first this shocked me well that students who are not yet have to much money to speed but later thinking about it makes me beleave that it is not from our country and many students have parttime jobs ans savings which they need to have save in a secure place which is the most importtant reason that they are th highest subscribtion and sbout retired people they well does have more money and does not what to room here there or to complicated tssks and with the free time they havae it give the bank more oportunity to convience them
--- 

## Track B — ML Engineer (Additional Questions)

### 3. Which feature had the highest importance in your tree-based model? Why do you think that is?

**`duration`** —The most important feature in the model was **duration**, which represents the length of the phone call with the customer. This makes sense because customers who spend more time on the call are usually more interested in the bank's offer and are more likely to subscribe to a term deposit. As a result, the model considered call duration to be the strongest indicator of whether a customer would subscribe or not.

---

### 4. Why is F1 a better metric than accuracy for this particular dataset?

With only 11.70% of customers subscribing, the classes are severely imbalanced. A model predicting "no" for everyone would score ~88% accuracy but have 0% recall for the class that actually matters. F1 balances precision (how many predicted "yes" were actually "yes") and recall (how many actual "yes" customers were caught), giving a single score that penalises the model for ignoring the minority class. For a bank trying to identify likely subscribers, missing real prospects (low recall) is just as costly as calling the wrong people (low precision).

---

### 5. Pick one of your 5 sample predictions. Do you actually agree with the model's call?

**Customer at index30441** — 55-year-old married blue-collar worker, secondary education, balance of €1,765, housing loan active, contacted by phone in February, call lasted 445 seconds, previous campaign outcome was a **failure**.

The model predicted **"no"** with 55.41% probability — essentially a coin flip. I partially agree with the call, but I'd flag this one as genuinely borderline. 
as the it has the highest importajce freture eith a great amont of value ,The long call duration (445s) and the fact he was contacted again after a prior failed campaign suggest some residual interest. On the other hand, blue-collar workers have the lowest overall subscription rate (7.27%) in this dataset, he carries a housing loan, and his last campaign outcome was explicitly "failure" — all signals pointing away from a subscription. The model's low confidence here reflects the real ambiguity in this customer's profile.

this prediction is best for seeing how the  model thinks as just perdictng no is easy and will work like 88 percent of time but  locking at the probability score thats the important part


---
