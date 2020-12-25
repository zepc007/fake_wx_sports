#### 打包命令
`打包命令为pyinstaller -Fw -i favicon.ico roma.py`
`
#### 运行窗口没有icon
- 1、创建favicon.qrc文件，写入以下内容：
```
<RCC> 
    <qresource prefix="/"> 
        <file>favicon.ico</file>
     </qresource> 
</RCC>
```
- 2、生成py文件，这个py文件把图片保存成二进制：
```shell
pyrcc5 favicon.qrc -o favicon.py
```
- 3、导入模块，设置图标
```python
import favicon
self.setWindowIcon(QIcon(':/favicon.ico'))
```

#### 涉及子线程及子进程的PyQt5程序打包后运行异常的解决方法
现象：创建子进程时，主进程无限重启
解决方案：在main函数中加一句话`multiprocessing.freeze_support()`
