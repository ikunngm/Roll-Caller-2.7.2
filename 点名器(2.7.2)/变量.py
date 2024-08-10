import pygame
pygame.init()

#创建一个屏幕并设置屏幕大小
screen = pygame.display.set_mode((1000,500))

#设置屏幕标题
pygame.display.set_caption("点名器")

#设置已关闭
set_enter = False

#未选择名单
list_already = False

#音乐已打开
music_switch = True

#音乐开关移动
move_music_switch_x = 0

#关闭快速三连抽
names_3_fast_switch = False

#关闭三连抽
names_3_switch = False

#三连抽未完成
names_3_already = False

#未点击"三连抽"
names_3_time = 0

#关闭快速幸运单抽
name_fast_switch = False

#关闭幸运单抽
name_switch = False

#幸运单抽未完成
name_already = False

#未点击"幸运单抽"
name_time = 0

#允许朗读
speak_switch = True

#朗读开关移动
move_speak_switch_x = 0

#停止朗读
speak_start = False

#音乐文件夹
music_folder = "音乐/"

#启动音乐文件夹
start_music_folder = "个性化/启动音乐/"

#背景文件夹
background_folder = "个性化/背景/"

#幸运单抽防重复列表
pass_names = []

#三连抽防重复列表
pass_names_3 = []

#设置界面特效X轴上移动的距离
move_set_x = 0

#设置界面特效y轴上移动的距离
move_set_y = 0

#背景X轴位置
photo_background_x = 0

#背景y轴位置
photo_background_y = 0

#状态栏阴影
music_state = pygame.Surface((1000,40),pygame.SRCALPHA)
music_state.fill((255,255,255,128))

#选音乐阴影
choose_music_state = pygame.Surface((250,100),pygame.SRCALPHA)
choose_music_state.fill((255,255,255,128)) 

#字体
font_30_size = pygame.font.Font("字体/HarmonyOS_Sans_SC_Light.ttf",30)

font_50_size = pygame.font.Font("字体/HarmonyOS_Sans_SC_Light.ttf",50)

#文本
text_help = font_30_size.render(("帮助"),True,(0,0,0))

text_about = font_30_size.render(("关于"),True,(0,0,0))

text_set = font_50_size.render(("设置"),True,(0,0,0))

text_back = font_30_size.render(("返回"),True,(0,0,0))

text_choose_list = font_50_size.render(("选名单"),True,(0,0,0))

text_names_3 = font_50_size.render(("三连抽"),True,(0,0,0))

text_name = font_50_size.render(("幸运单抽"),True,(0,0,0))

text_choose_music = font_50_size.render(("选音乐"),True,(0,0,0))

text_music_switch_on = font_30_size.render(("音乐已打开"),True,(0,0,0))

text_music_switch_off = font_30_size.render(("音乐已关闭"),True,(0,0,0))

text_speak_switch_on = font_30_size.render(("朗读已打开"),True,(0,0,0))

text_speak_switch_off = font_30_size.render(("朗读已关闭"),True,(0,0,0))

warn_list = font_50_size.render(("请选择名单"),True,(0,0,255))