import streamlit as st

def main():
    # Set the title of the page
    st.title('About the Project')

    # Goal of the project
    st.header('Goal of the Project')
    st.markdown('''
                To predict whether a bank customer will **subscribe to a term deposit**('yes' or 'no') after being contacted during a direct marketing campaign.
                
                - Binary classification problem
                - Highly imbalanced data (~11% subscribed)
                - The goal is to develop a model that balances **recall**, **precision** and **interpretability** to make it suitable for **deployment**
                ''')
    st.markdown("---")
    # Dataset overview
    st.header('Dataset Summary')
    st.markdown('''
                This project uses the **UCI Bank Marketing - Additional(Full) * from UCI, **not** the simpler 'bank.csv' version.

                **File used**: 'bank-additional-full.csv'

                **Source**: [https://archive.ics.uci.edu/dataset/222/bank+marketing](https://archive.ics.uci.edu/dataset/222/bank+marketing)
               ''')
    
    st.markdown('''
               ### Dataset Highlights
               - 41,188 records with detailed client and economic features
               - Includes macroeconomic indicators
               - Provides realistic model challenges (class imbalance, missing categories)
               - Great for SHAP interpretability and model evaluation
                ''')
    
    st.image('images/class_distribution.png', caption='Target Class Distribution (~11% subscribed)')

    # Data Quality and Preprocessing
    st.header('Data Quality & Preprocessing')

    st.markdown('''
               -**Duplicates**: Found 12 - kept due to their minimal impact
                
               -**Missing/unknown values**:
                  - 'default': 8,597
                  - 'education': 1731
                  - 'housing', 'loan': 999
                  - 'job': 300
                  - 'marital': 80
                  → kept initially and monitored with SHAP
                
                -**Outliers**: Present in 'duration', 'campaign', etc.

                  → kept initially because the positive class is a rare event and they might serve as important predictors
                ''')
    st.image('images/boxplots.png', caption='Boxplots of numeric features')

    st.markdown('''
                -**Correlation Insights**
                
                Several features showed strong correlation - especially among macroeconomic indicators:
                - `euribor3m` and `nr.employed`  
                - `emp.var.rate` and `cons.conf.idx`

                These could affect linear models or inflate feature importance.

                → kept initially and addressed during the modeling stage since I would use both linear and non-linear models
                ''')
    st.image('images/correlation_heatmap.png', caption='Correlation heatmap of numeric features')


    # Dimensionality Reduction
    st.header('Dimensionality Reduction')
    st.markdown('''
                Used **PCA**, **LDA** and **UMAP** to explore linear and non linear class structure and separability.
                
                - No strong separation was observed across methods

                - As a result, I **deprioritized oversampling**(e.g. SMOTE), since it could introduce unnecessary noise
                ''')
    
    projection = st.selectbox('Choose a projection method' ,['PCA', 'LDA', 'UMAP'])

    if projection == 'PCA':
        st.image('images/pca.png', caption='PCA')
    
    elif projection == 'LDA':
        st.image('images/lda.png', caption='LDA')
    
    else:
        st.image('images/umap.png', caption='UMAP')

    # Feature Engineering
    st.header('Feature Encoding & Scaling Strategy')
    st.markdown('''
                To prepare the data for different models, I built **separate preprocessing pipelines**:
                
                -**Categorical Encoding**:
                 - Used `OneHotEncoder` to convert categorical features into numeric format
                 - For linear model, dropped the **first category** to avoid multicollinearity
                 - For tree-based models, kept all categories (no need to drop because they are non-linear)
                
                -**Numerical Scaling**:
                 - Applied `RobustScaler` to reduce the influence of outliers
                 - For more details about `RobustScaler`, check the link below:
                
                 → https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.RobustScaler.html
                 - Tree-based models used raw values (they are scale-invariant)
                ''')
    
    # Modeling & Evaluation
    st.header('Modeling & Evaluation')
    st.markdown('''
                I built multiple models and refined them through an iterative evaluation process:

                ### Baseline Model:
                - Trained: `Logistic Regression`, `SVM(LinearSVC)`, `Random Forest`,`XGBoost`
                - Metric: **F1 Score** (due to class imbalance)
                - All models performed poorly (F1 < 0.4)       
                ''')
    st.image('images/base.png', caption='F1 scores of Baseline Models')

    st.markdown('''
                ### Handling Imbalance:
                - Used **class_weight='balanced'**(instead of oversampling)

                → justified by lack of clear structure in dimensionality reduction
                ''')
    st.image('images/balanced.png', caption='Comparison of F1 Scores for Baseline vs Balanced Models')

    st.markdown('''
               - Tested **SMOTE**
               
               → Since balanced Models didn't perform well
                ''')
    st.image('images/smote.png', caption='Comparison of F1 Scores for Baseline vs Balanced vs SMOTE Models')

    st.markdown('''
                ### Feature Selection:
                - For **linear models**, removed features with correlation > 0.8
                - **Tree-based** models retained all features
                - Selected following models as top 5 models (highlighted by red) based on F1, and interpretability
                  - `Balanced XGBoost`
                  - `SMOTE SVM` (correlation-filtered)
                  - `SMOTE Logistic Regression` (correlation-filtered )
                  - `Balanced Logistic Regression` (correlation-filtered)
                  - `Balanced SVM` (correlation-filtered)
                - `Balanced SVM` (**without correlation filtering**) and `SMOTE SVM` (**without correlation filtering**) have high F1 scores
                  but because of **multicollinearity**, it's hard to interpret. Therefore, I excluded them from the top 5 models.
                ''')
    st.image('images/corr.png', caption='Comparison of F1 Scores for Baseline vs Balanced vs SMOTE vs Corr-Filtered Models')

    st.markdown('''
                ### Model Tuning:
                - Tuned the top 5 models
                - Used **Bayesian Optimization** for hyperparameter tuning
                  - For more details about Bayesian Optimization, check the link below:
                
                  → https://scikit-optimize.github.io/stable/modules/generated/skopt.BayesSearchCV.html
                
                - Evaluated models using **Precision-Recall AUC** and **custom thresholds**
                  - This is because the target class is **highly imbalanced** and ROC AUC does not effectively reflect the model performance
            
                - For better visualization, the following two graphs are shown:
                  - **LEFT**: Top 3 models based on AUC scores after tuning from the top 5 models
                  - **Middle**: Top 1 models based on AUC scores after tuning from the top 5 models
                  - **RIGHT**: All the top 5 models
                ''')
    st.image('images/prauc_1.png', caption = 'Precision-Recall curves from top 5 models after tuning')

    st.markdown('''
                **Note**: According to the graph and this investigation, I will focus on the following 3 models for further evaluation:
                   - `Balanced_XGBoost_tuned_1`
                   - `SMOTE_Logistic_Regression_corr_tuned_1` 
                   - `SMOTE_SVM_corr_tuned_1` 
                - Balanced_XGBoost and SMOTE_Logistic_Regression_corr rank as the top 2 performers by AUC score, and both perform stably across the PR curve.
                - Although Balanced_Logistic_Regression_corr shows similar overall performance, it exhibits a sharp drop at a specific threshold, indicating instability in its precision-recall trade-off.
                - Since reliable performance across thresholds matters for business decisions, I'll exclude it in favor of the three models above.
                - To illustrate the improvement in F1 scores, the following 3 graphs are shown:
                  - **LEFT**: Baseline models (F1 Scores)
                  - **MIDDLE**: Top 5 models before Tuning (F1 Scores)
                  - **RIGHT**: Top 3 models after Tuning (F1 Scores with the best thresholds)
                ''')
    st.image('images/f1_first_tuned.png', caption = 'Comparison of F1 Scores for Baseline vs  Top 5 models before Tuning vs  Top 3 models after Tuning')
    # Additional feature engineering
    st.header('Additional Feature Engineering')
    st.markdown('''
                After selecting promising models and tuning hyperparameters, I performed further **feature engineering** to improve performance.
                - **Combining features**
                  - **job_marital** → This could indicate lifestyle and financial situation
                  - **housing_marital** → This could indicate stability of life situation
                  - **contact_month** → This could indicate the interaction between months and contact methods
                
                - **Applying a log and a square root transformation** 
                  - Applied **a log transformation** to **campaign**, as it does not contain zero
                  - Applied **a square root transformation** to **previous**, as it contains zero
                  - These transformations don't make the distributions symmetrical, but they do help reduce the impact on extreme values without changing the overall shape of the distributions. 
                  - You can see the before-and-after effect of these transformations in the graph below:
                ''')
    st.image('images/log_transformation.png', caption ='Log and square root transformation before and after')
  
    # Feature Engineering Impact Evaluation
    st.header('Evaluating the Impact of Feature Engineering')
    st.markdown('''
                - After applying additional feature engineering, I retrained and tuned the top 3 models from earlier
                - To assess the impact of feature engineering, I compared **PR AUC curves** of the top 3 models with and without the additional feature engineering
                - For better visualization, the following two graphs are shown:
                 - **LEFT**: Top 3 models based on AUC scores 
                 - **MIDDLE**: Top 4 models based
                 - **RIGHT**: All 6 models, namely:
                   - `Balanced_XGBoost_tuned_1` 
                   - `SMOTE_Logistic_Regression_corr_tuned_1` 
                   - `SMOTE_SVM_corr_tuned_1` 
                   - `Balanced_XGBoost_f1` (**With additional feature engineering**)
                   - `Balanced_Logistic_Regression_corr_f1` (**With additional feature engineering**)
                   - `SMOTE_SVM_corr_f1` (**With additional feature engineering**)
               ''')
    st.image('images/prauc_2.png', caption = 'Precision-Recall curves from top 3 models with and without additional feature engineering' )
    st.markdown('''
                - **Balanced_XGBoost** and **Balanced_XGBoost_f_1** are the most stable models and rank highest by AUC.
                - By AUC, SMOTE_SVM_corr_f1 ranks third, but it shows a sharp drop near low recall, indicating it is not as stable across thresholds.
                - So I will select the best model between **Balanced_XGBoost** and **Balanced_XGBoost_f_1**.
                ''')
    
    # Decide the best model 
    st.header('Decide the Best Model')
    st.markdown('''
                - I applied the best threshold to all 3 models based on their F1 scores
                - I plotted a comparison of the best F1 scores
                - I also included the **baseline models** to visualize how much the performance improved 
                  - **LEFT**: Baseline models 
                  - **RIGHT**: Top 3 models 
                ''')
    st.image('images/final_model.png', caption='Comparison of F1 Scores for Baseline vs Final top 3 models + SVM (Reference)')
    st.markdown('''
                - **Best Model: `Balanced_XGBoost_tuned_1`**
                - Among the top-performing models, the **XGBoost variants** achieved **the highest F1 scores** with minimal performance difference.
                - The `Balanced_XGBoost_tuned_f1` model includes **additional features from feature engineering**, while `Balanced_XGBoost_tuned_1`
                   relies only on **the original features**
                - Since both models perform similarly, I selected **`Balanced_XGBoost_tuned_1`** as the final model for it's **better interpretability**,
                   as it uses only the original features
                ''')

    # Model interpretability 
    st.header('Model Interpretability with Feature Importance and SHAP')
    st.markdown('''
                - The following graphs are shown:
                  - **Left**: Feature Importance based on model-specific method (XGBoost gain)
                  - **Right**: Mean |SHAP| value (model-agnostic feature influence)
                ''') 
    st.image('images/feature_importance.png', caption='Feature Importance & Mean |SHAP| value')
    st.markdown('''
                - Although both plots highlight **num_nr.employed** as the most import feature, SHAP reveals different insights compared to traditional feature importance
                - For example, **cat_contact_cellular** and **num_cons.price.idx** have low importance in the left plot but rank higher in SHAP, meaning they consistently influence
                  predictions across may instances
                - SHAP can capture subtle but consistent influence missed by split-based importance, and unlike traditional plots, SHAP shows **directional influence**, explored next
                ''')
    
    st.header('SHAP Plot with Direction')
    st.markdown('''
                - The SHAP swarm plot below adds **directionality** to feature influence
                - Each dot is a SHAP value for one instance, colored by feature value (blue = low, red = high)
                ''')   
    
    st.image('images/shap_1.png', caption='SHAP swarm plot')
    st.markdown('''
                ### Insights
                
                1. **num__nr.employed**: Low values increase prediction probability. This might reflect higher subscription rates during unstable economic periods.
                2. **cat__contact_cellular**: Mobile contact increases success likelihood.
                3. **num__cons.price.idx**: Higher inflation reduces subscription probability.
                4. **num__cons.conf.idx**: Low confidence increases likelihood, suggesting clients prefer secure investments when uncertain.
                5. **num__campaign / num__previous**: More contacts reduce success.
                6. **num__pdays**: Recent contact boosts likelihood of subscription.
                ''')   

    st.header('SHAP Plots for True Positives (TP)')
    st.markdown('''
                - The model's F1 score is ~0.5, so it's important to understand when predictions are correct
                - Below is the SHAP plot for **true positives (TP)** -cases where the model correctly predicted a subscription
                - This plot shows direction and strength of influence for TP predictions. 
                ''')
    st.image('images/shap_2.png', caption='SHAP swarm plot for True Positives (TP)')
    st.markdown('''
                ### Insights

                1. **num__nr.employed**: Direction unclear, despite strong average influence.
                2. **num__pdays**: Low values strongly boost success.
                3. **num__cons.conf.idx**: Low confidence continues to raise success likelihood.
                4. **cat__contact_cellular**: Presence of mobile contact pushes prediction higher.
                5. **cat__day_of_week_mon**: Not contacting on Monday is more effective.
                6. **cat__month_oct**: October contact raises success probability.
                ''')

    # Apply the Model to the Test set
    st.header('Apply the Model to the Test Set')
    st.markdown('''
               - The following graphs visualize model improvement and performance:
                 - **LEFT**: Baseline models
                 - **MIDDLE**: Final top 3 models + SVM(reference)
                 - **RIGHT**: Final model on test set
               ''')
    st.image('images/test.png', caption='Baseline models vs Final top 3 models + SVM(reference) vs Final model on test set')
    st.markdown('''
                ### Conclusion and Test Set Performance
                - After extensive tuning, **XGBoost(balanced_tuned)** was selected as the final model.
                  - **Train F1 Score:** 0.494
                  - **TEST F1 Score:** 0.519
                
                This reflects good generalization and robust performance for an imbalanced classification task.
                
                ## Key Takeaways
                1. **Tuning and rebalancing** (SMOTE, class_weight, Bayesian Optimization) significantly improved all models.
                2. **XGBoost** outperformed others on both training and test sets.
                3. **SHAP analysis** provided deep insights into feature behavior and model decision-making-
                4. The model is a solid foundation, but further improvement can come from:
                   - Collaborating with marketing/domain teams to validate SHAP insights
                   - Incorporating new features based on expert input
                   - Continuous feedback from real-world deployment to refine strategy
                ''')
# Allow this file to be tested on its own
if __name__ == "__main__":
    main()
