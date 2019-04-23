# 修改文件
        papershow\src\material\src\config.py
        src\chn_classify_workspace\tag_paper_chn.py
# config文件
      done.txt存取上次任务是否执行完毕
      task.txt存取当前任务id
# user_input
用户输入时间段 or 库名后，点击提交；
后台查询当前要处理多少篇文档，再次点击运行开始对数据进行深加工；

        1. 从task.txt中读取当前任务id存入 task_id
        2. 读取当前要处理的pdf路径并存入 results
        3. (1) 将results内容存入“MirrorFileInfo表”
           (1) 每次处理pdf_num篇文档
           (2) 将pdf_num篇文档存入size个文件夹中（并发数为size） 
           (3) 并行运行size-1个进程运行bat程序，最后的一个
               进程与之前一个串行运行
           (4) bat程序包含：
               a:将一个文件夹下的pdf处理为xml
               b:
