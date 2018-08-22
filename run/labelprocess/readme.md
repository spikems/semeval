labelprocess
==============

## Background

目前有两批正负面数据文件，其中汽车行业的数据共1,006,170条，负面标注共21,886，占比约2.2%.
按讨论，预计数据集中负面标注recall不足，需要通过进一步标注修订来提高训练集质量。
一个迭代修订步骤如下：

- 数据组制定标注规则。针对汽车行业一般性的需求，区分负面/非负面的标准。

- 我从数据集中取一个子集N，规模在20,000左右，请数据组标注。

- 得到新标注结果，我去更新训练集，并分析质量判断是否结束修订，否则转步骤2

质量判断的方法：

- 假设已有负面的样本准确度高，修订的目标主要是找到那些应该是负面，但没有被标注为负面的样本。（同时，也给出一批高准确度的非负面样本）

- 在全部数据集上构建分类器，通过分类预测结果找到三个子集A:高概率预测为负面，但原始标注非负面，B:高概率预测为非负面，C: 分类的模糊边界。遗漏的负面样本出现在{A,C}中间可能性大，从中取前N个作为待标注集合。（尝试把B不经过人工修订，直接作为标注数据，减少一些标注工作量。）

- 经过标注的数据作为训练集，检查分类性能，预计能观察到性能的变化，从中来估计新加入的标注数据的影响程度。当影响变小的时候，迭代终止。

## usage

```sh

#prepare the original .xlsx makeup dataset under ../dataset
#make the initial version of labelset
make_labelset_v1.sh

#when the labelset get feedback, go forward to the next versions
go_nextiter 1
go_nextiter 2

#finish iterations, and output the latest version of trainset
final_trainset 2


```

