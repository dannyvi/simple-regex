说明
======

##语法制导翻译（SDD）

写一个NFA（非确定有穷自动机）的正则表达式引擎，可以用graphviz展示状态图，可以用
样式生成自动机。可以用生成的nfa对字符串进行匹配。


过程：
    
对pattern(样式)进行LR规约，在规约过程对样式进行语法制导翻译
(Syntax Directed Translation)，生成该样式的状态机。

组成状态图和状态机的基本构件 ``graph.py``：

    class State:
    class Path: 
    class Graph:
    class Machine:
    
构建nfa的基本规则 ``regex_nfa.py``:

    basis
    
    induct_or
    induct_cat
    induct_star
    
正则表达式的规范(LR1)语法分析表 ``parsing_table.py``:

    get_states_map
    
将输入按照语法分析表进行规约，并在规约过程并入语义动作。

