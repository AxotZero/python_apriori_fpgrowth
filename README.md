# Report

## Find and answer
What do you observe in the below 4 scenarios? (For both support and confidence, High and Low are arbitrary choices; you may set them according to your preference)
* High support, high confidence
* High support, low confidence
* Low support, low confidence
* Low support, high confidence
* Any topics you are interested in

### 產出 ibm association rule
- `min_support` = 0.1, `min_confidence` = 0.01 產出 association rules
    - ![](https://i.imgur.com/NxZLPsZ.png)

### 選取 `low_support`, `high_support`, `low_confidence`, `high_confidence`
- 以 quantile 過後的 `support` 與 `confidence` 取值
    - ![](https://i.imgur.com/FK6Agmq.png =200x)
    - 0.2的位置當作 low, 0.8當作 high，最後得到 threshold
        - low_support(ls): 0.107
        - high_support(hs): 0.152
        - low_confidence(lc): 0.198
        - high_confidence(hc): 0.582
- 

### 四種 scenarios


| sup/ <br />con | low | high |
| -------- | -------- | -------- |
| low     | ![](https://i.imgur.com/HjcNpTj.png)     | ![](https://i.imgur.com/TbiBY6w.png)     |
| high     | ![](https://i.imgur.com/qS6akFn.png)     | ![](https://i.imgur.com/Qi1dypI.png)     |

我為 association_rule 新增了兩個 column `ant_count`, `con_count` 分別代表 antecedent 與 consequent 的 item_set 的長度，以下列出我觀察到的現象:
- **support 對 confidence 的影響**
    - 當整體 item_set support 越高時，代表那些 item_set 越常出現，也就代表 item_set 同時出現的機率越高，反之亦然，因此會發現，
        - lslc 與 hshc 數量最多
        - lshc 數量也還行，畢竟 support 可以不高，但相關的 item_set 能夠一起出現
        - hslc 最少，如果把 threshold 再往兩邊調一點的話，就完全沒有這種資料出現了(low_quantile=0.16, high_quantile=0.84)
- **support 對 ant_count 和 con_count 的影響**
    - 可以看到 low_support 會造成 ant_count 接近 2，con_count > 4；而 high_support 使 ant_count 和 con_count 接近 3, 
    - confidence 似乎沒啥影響 
    - 只觀察這四種狀況下這種結論可能不太對，不過我有點懶了。


## 嘗試產出上述四種特性的 data
### 產生假資料
我將 `ntrans` 固定為 10 並以下列參數產生假資料
| tlen | nitems | 
| -------- | -------- | 
| 4     | 60     | 
| 20     | 300     | 
| 4     | 300     | 
| 20     | 60     | 

> 其他的參數: `npats`, `patlen`, `corr`, `conf` 有調跟沒調，產出來的結果根本差不多，不知道哪裡有問題qq

### 共同現象
- item_set 的長度越長，其 support 越低
- rule 的 consequent 長度越長 && antecedent 越短，其 confidence 越低

### 四組 data 的比較
- `(4, 60)`, `(20, 300)` 產出來的 rule 的 support 與 confidance 差不多，但 `(20, 300)` 產生出的 rule 比較多，畢竟組合比較多
-  `(4, 300)` 產出來的有 (low_support, low_confidance) 與 (low_support, high_confidance)，不過 (low_support, high_confidance) 出現的次數不多。
-  `(20, 60)` 為 (high_support, high_confidance)，畢竟 item 數量很少，且 transaction 及 transaction_len 都很高，蠻不意外的
- 直到最後我依然沒有產生出 high_support, low_confidance 的資料，`-conf` 有調跟沒調一樣
    - 我自己認為，依照兩者的特性，support 越高代表該 item_set 越常出現， confidance 越高，代表兩個 item_set 同時出現的次數越高，若是每個 item_set 都很常出現，那麼他們同時出現的機率也會提高
    - 應證了 ibm-2022 的分析
    - 花了好幾個小時想找出這種組合，但我最後放棄了
    
## Bonus
- 資料來源: [kaggle-groceries-dataset](https://www.kaggle.com/datasets/heeraldedhia/groceries-dataset
- `min_support` = 0.01, `min_confidence` = 0.01 產出 association rules
    - ![](https://i.imgur.com/7TDAoUS.png)
- 將各個 columns quantile 來看
    - ![](https://i.imgur.com/jLqe9Ri.png)
    - 是偏向 low_support, high_confidence 的 data 呢 ~!

