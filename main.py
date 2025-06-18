import os.path
import threading
from tkinter import Label, Button, Toplevel
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showerror
from tkinter.ttk import Progressbar

from ncm_converter import log, dumpfile


def select_file():
    log.info("单文件模式")
    file_path = askopenfilename(title="请选择要转换的文件",
                                initialdir="C:\\CloudMusic\\VipSongsDownload" if os.path.exists(
                                    "C:\\CloudMusic\\VipSongsDownload") else None,
                                filetypes=[("网易云音乐文件", "*.ncm")])
    if file_path:
        log.info(f"文件路径： {file_path}")
        output_dir = askdirectory(title="选择保存目录",
                                  initialdir=os.path.expanduser("~") if os.name == "nt" else os.path.expanduser(
                                      "~/Documents"),
                                  mustexist=True if os.name == "nt" else False)
        log.info(f"保存路径： {output_dir}")
        if output_dir:
            # 创建不可关闭的等待窗口
            wait = Toplevel()
            wait.title("请稍后")
            wait.protocol("WM_DELETE_WINDOW", lambda: None)  # 禁止关闭窗口
            Label(wait, text="请稍后").pack(padx=50, pady=20)
            wait.transient()  # 设置为临时窗口（模态）
            wait.grab_set()  # 抢占焦点
            wait.update()

            try:
                dumpfile(file_path, output_dir)
            finally:
                wait.destroy()
        else:
            log.error("用户未选择输出文件")
            showerror("错误", "请选择一个有效的输出目录")
    else:
        log.error("用户未选择源文件")
        showerror("错误", "请选择一个有效的文件")


def select_folder():
    """
        处理单文件转换流程

        功能流程:
        1. 弹窗选择.ncm文件
        2. 弹窗选择输出目录
        3. 调用dumpfile进行转换
        4. 显示转换进度窗口

        异常处理:
        - 用户未选择文件/目录时弹窗提示错误
        - 转换过程异常记录日志并显示错误对话框
        """
    input_folder = askdirectory(title="请选择要转换的文件夹",
                                initialdir="C:\\CloudMusic\\VipSongsDownload" if os.path.exists(
                                    "C:\\CloudMusic\\VipSongsDownload") else None)
    if not input_folder:
        log.error("用户未选择输入文件夹")
        showerror("错误", "请选择一个有效的输入文件夹")
        return

    output_folder = askdirectory(title="请选择输出目录")
    if not output_folder:
        log.error("用户未选择输出文件夹")
        showerror("错误", "请选择一个有效的输出文件夹")
        return

    # 过滤NCM文件
    ncm_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.ncm')]
    if not ncm_files:
        showerror("错误", "输入文件夹中没有NCM文件")
        return

    # 创建进度窗口
    progress_window = Toplevel()
    progress_window.title("转换进度")
    progress_window.geometry("300x100")
    progress_window.transient()
    progress_window.grab_set()
    progress_window.destroyed = False  # 添加自定义属性

    # 进度条组件
    progress = Progressbar(progress_window, orient="horizontal", length=250, mode="determinate")
    progress.pack(pady=20)
    progress["maximum"] = len(ncm_files)

    # 状态标签
    status_label = Label(progress_window, text="正在初始化...")
    status_label.pack()

    # 转换线程函数
    def convert_thread():
        try:
            for i, file_name in enumerate(ncm_files):
                if not progress_window.winfo_exists():  # 先检查窗口是否存在
                    break
                if getattr(progress_window, 'destroyed', False):  # 使用安全访问
                    break

                status_label.config(text=f"正在转换：{file_name}")
                progress_window.update()

                input_path = os.path.join(input_folder, file_name)
                try:
                    dumpfile(input_path, output_folder)
                    log.info(f"转换成功：{file_name}")
                except Exception as err:
                    log.error(f"转换失败：{file_name}: {str(err)}")

                progress["value"] = i + 1
                progress_window.update()

            progress_window.after(0, lambda: (
                status_label.config(text="转换完成！"),
                progress_window.after(1500, progress_window.destroy)
            ))
        except Exception as e:
            log.error(f"批量转换异常：{str(e)}")
            progress_window.after(0, lambda exc=e: (  # 捕获异常变量
                showerror("错误", f"转换过程中发生错误：{str(exc)}"),
                progress_window.destroy()
            ))

    # 启动转换线程
    thread = threading.Thread(target=convert_thread, daemon=True)
    thread.start()


tk = Tk()
tk.title("网易云音乐转码工具")
Label(tk, text="网易云音乐转码工具GUI版本").pack()

# 在主界面按钮绑定时添加点击日志
Button(tk, text="选择文件", command=lambda: [log.info("用户点击[选择文件]按钮"), select_file()]).pack()
Button(tk, text="选择文件夹", command=lambda: [log.info("用户点击[选择文件夹]按钮"), select_folder()]).pack()

Button(tk, text="退出", command=tk.quit).pack()
tk.mainloop()
