import os

def compile_ui():
    ui_path = './ui/'
    names = os.listdir(ui_path)
    print(names)
    for name in names:
        print(name)
        for directory in os.listdir(ui_path + name):
            print(directory)




if __name__ == '__main__':
    compile_ui()
