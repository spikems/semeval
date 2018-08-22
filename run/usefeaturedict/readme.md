usefeaturedict
=================

build a new engine for feature extracting

## procedure:

- start from cws with new word dictionary
- feature selection
- maintain NZ-Dictionary: brand name, NZ(person name, location name, number, time)
    - It's a easy task here, no need to build a full featured NER but find out all NZ in the training set.
    - filtering (remove by/save to NZ-Dictionary), Noise-Dictionary(remove list)
    - maintain Syntax-Dictionary: 否定，转折，想象，比较
    - 找到这些语法现象的pattern, 用于提取正确的特征

    - 处理指代关系，表达为Target-Feature的组合特征
    目前只想到简单的窗口，以及向后覆盖

    - 最基本的sentiment 信息，还是Aspect Dictionary 和 Opinion-Ditionary.
    - 简化问题，不需要aspect-opinion pair, maintian dictionary for tagging only
    - combine the tagged features is another procedure.

    - 处理扩展性问题，就是新数据中未被training set covered的feature如何加入问题
    use feature-pattern to generalize the model, like target-aspect-opinion
    what's the difference? using syntax rules .vs. maintain a aspect, opinion dictionary .vs. data driven?
    assumption: the training set covered typical expression patterns and words.
        data driven seems better: use dictionary other than use rules
            dictionary is easy to extend, don't worry about the space and coverage
        simple syntax recognition: use dictionary other than use rules
            aspect, opinion all using dictionary to recognize
            否定，转折，想象，比较, using dictionary too
    -target-aspect-opinion 也不要严格rules, but n-gram like方式的组合即可，extract by <opinion, aspect, target> 元组为特征片段

## solution:

    - simple cws with basic dictionary, close ner (to recall all possible important features)
    - NZ-dictionary, Aspect, Opinion Dictionary(mining, newword finder from trianing set, extended by maintenance)
    - Syntax-Dictionary(close form)
    - tagger
    - feature extractor on tag sequence
