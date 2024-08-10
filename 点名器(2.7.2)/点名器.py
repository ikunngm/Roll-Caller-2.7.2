from chardet.universaldetector import UniversalDetector
import pyttsx3,pygame,time,sys,os,re
from tkinter import filedialog
from random import choice
from 变量 import*
#检测音乐文件名称
music_list = os.listdir(music_folder)
for music in music_list:
	if music.endswith(".mp3"):
		music_path = music_folder + music
text_music_name = font_30_size .render(("当前的音乐是:" + music),True,(0,0,0))
music_last = music_path
#默认背景
def build_background():
	pygame.draw.rect(screen,(239,136,190),(photo_background_x,photo_background_y,1000,500),0)
try:	
	#检测启动音乐文件名称
	start_music_list = os.listdir(start_music_folder)
	for start_music in start_music_list:
		if start_music.endswith(".mp3"):
			start_music_path = start_music_folder + start_music
	#播放启动音乐
	pygame.mixer.music.load(start_music_path)
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play()
finally:
	try:
		#检测背景文件名称
		background_list = os.listdir(background_folder)
		for background in background_list:
			if background.endswith(".jpg") or background.endswith(".png"):
				background_path = background_folder + background
		#用户自定义背景
		photo_background = pygame.image.load(background_path).convert()
		def build_background():
			screen.blit(photo_background,(photo_background_x,photo_background_y))
	finally:	
		while True:
			for user_input in pygame.event.get():	
				mouse = pygame.mouse.get_pos()
				#退出
				if user_input.type == pygame.QUIT:	
					pygame.quit()
					try:
						os.remove(r"临时名单.txt")
					finally:
						sys.exit()
				#点击判定
				if user_input.type == pygame.MOUSEBUTTONDOWN:	
					#选名单
					if 0 <= mouse[0] <= 250 and 400 <= mouse[1] <= 500:
						#设置已关闭
						if set_enter == False:
							#防止三连抽或幸运单抽运行时其他按钮被点击造成卡死
							#关闭快速三连抽
							names_3_fast_switch = False
							#关闭三连抽
							names_3_switch = False
							#未点击"三连抽"
							names_3_time = 0
							#关闭快速幸运单抽
							name_fast_switch = False
							#关闭幸运单抽
							name_switch = False
							#未点击"幸运单抽"
							name_time = 0
							#停止朗读
							speak_start = False
							#停止音乐
							pygame.mixer.music.stop()
							#绘制白色按钮特效矩形
							pygame.draw.rect(screen,(255,255,255),(0,400,250,100),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#绘制黑色按钮特效矩形
							pygame.draw.rect(screen,(0,0,0),(0,400,250,100),1)
							#更新屏幕
							pygame.display.update()
							#选名单窗口
							names_list = filedialog.askopenfilename(title = "请选择名单", filetypes = [("文本文档",".txt")])
							if names_list != "":
								#不带后缀的名单文件名
								names_list_name = os.path.basename(names_list)
								text_names_list = font_30_size .render(("当前的名单是:" + names_list_name),True,(0,0,0))
								#检测名单文件字体类型
								try_text = UniversalDetector()
								try_text.reset()
								for test_txt in open(names_list,"rb"):
									try_text.feed(test_txt)
									if try_text.done:
										break
								try_text.close()
								#判断名单文件是否需要更改为utf-8
								if try_text.result["encoding"] != "utf-8":
									#创建一个临时文件
									names_list_utf_8 = open("临时名单.txt", "w")
									open_names_list = open(names_list,"r",errors = "replace")
									text_read = open_names_list.read()
									open_names_list.close()
									#将名单文件以utf-8写入临时文件
									names_list_utf_8 = "临时名单.txt"
									write_names_list_utf_8 = open(names_list_utf_8,"w",encoding = "utf-8",errors = "replace")
									write_names_list_utf_8.write(text_read)
									write_names_list_utf_8.close()
								else:
									names_list_utf_8 = names_list
								names_list_last = names_list
								#已选择名单
								list_already = True
								#三连抽未完成
								names_3_already = False
								#幸运单抽未完成
								name_already = False
							else:
								if list_already == True:
									names_list = names_list_last
					#三连抽
					if 250 <= mouse[0] <= 500 and 400 <= mouse[1] <= 500:	
						#设置已关闭
						if set_enter == False:
							#已选择名单
							if list_already == True:
								#防止幸运单抽运行时"三连抽"被点击造成卡死
								#关闭快速幸运单抽
								name_fast_switch = False
								#关闭幸运单抽
								name_switch = False
								#幸运单抽未完成
								name_already = False
								#未点击"幸运单抽"
								name_time = 0
								#第1次点击"三连抽”
								names_3_time += 1
								#音乐开关已打开
								if music_switch == True:
									#继续播放
									pygame.mixer.music.unpause()
									play = pygame.mixer_music.get_busy()
									#播放
									if play == False:    
										#播放音乐
										pygame.mixer.music.load(music_path)
										pygame.mixer.music.set_volume(0.5)
										pygame.mixer.music.play()
								#第1次点击启动快速三连抽+关闭三连抽+三连抽未完成+不允许朗读
								if names_3_time == 1:
									names_3_fast_switch = True
									names_3_switch = False
									names_3_already = False
									speak_start = False
								#第2次点击启动三连抽+关闭快速三连抽+未点击"三连抽"
								if names_3_time >= 2:
									#暂停音乐
									pygame.mixer.music.pause()
									names_3_switch = True
									names_3_fast_switch = False
									names_3_time = 0
					#幸运单抽
					if 500 <= mouse[0] <= 750 and 400 <= mouse[1] <= 500:
						#设置已关闭
						if set_enter == False:
							#已选择名单
							if list_already == True:
								#防止三连抽运行时"幸运单抽"被点击造成卡死
								#关闭快速三连抽
								names_3_fast_switch = False
								#关闭三连抽
								names_3_switch = False
								#三连抽未完成
								names_3_already = False
								#未点击"三连抽"
								names_3_time = 0
								#第1次点击"幸运单抽”
								name_time += 1
								#音乐开关已打开
								if music_switch == True:
									#继续播放
									pygame.mixer.music.unpause()
									play = pygame.mixer_music.get_busy()
									#播放
									if play == False:    
										#播放音乐
										pygame.mixer.music.load(music_path)
										pygame.mixer.music.set_volume(0.5)
										pygame.mixer.music.play()
								#第1次点击启动快速幸运单抽+关闭幸运单抽+幸运单抽未完成+不允许朗读
								if name_time == 1:
									name_fast_switch = True
									name_switch = False
									name_already = False
									speak_start = False
								#第2次点击启动幸运单抽+关闭快速幸运单抽+未点击"幸运单抽”
								if name_time >= 2:
									#暂停音乐
									pygame.mixer.music.pause()
									name_switch = True	
									name_fast_switch = False
									name_time = 0
					#设置
					if 750 <= mouse[0] <= 1000 and 400 <= mouse[1] <= 500:
						#设置已关闭
						if set_enter == False:
							#防止三连抽或幸运单抽运行时其他按钮被点击造成卡死
							#关闭快速三连抽
							names_3_fast_switch = False
							#关闭三连抽
							names_3_switch = False
							#未点击"三连抽"
							names_3_time = 0
							#关闭快速幸运单抽
							name_fast_switch = False
							#关闭幸运单抽
							name_switch = False
							#未点击"幸运单抽"
							name_time = 0
							#停止朗读
							speak_start = False
							#停止音乐
							pygame.mixer.music.stop()
							#绘制白色按钮特效矩形
							pygame.draw.rect(screen,(255,255,255),(750,400,250,100),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#绘制黑色按钮特效矩形
							pygame.draw.rect(screen,(0,0,0),(750,400,250,100),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#设置已打开
							set_enter = True
					#返回				
					if 0 <= mouse[0] <= 100 and 0 <= mouse[1] <= 50:
						#设置已打开
						if set_enter == True:
							#绘制白色按钮特效矩形
							pygame.draw.rect(screen,(255,255,255),(0,0,100,50),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#绘制黑色按钮特效矩形
							pygame.draw.rect(screen,(0,0,0),(0,0,100,50),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#设置已关闭
							set_enter = False
					#选音乐				
					if 0 <= mouse[0] <= 250 and 90 <= mouse[1] <= 190:
						#设置已打开
						if set_enter == True:
							#音乐开关已打开
							if music_switch == True:
								#绘制白色按钮特效矩形
								pygame.draw.rect(screen,(255,255,255),(0,90,250,100),1)
								#更新屏幕
								pygame.display.update()
								#特效延迟
								time.sleep(0.1)
								#绘制黑色按钮特效矩形
								pygame.draw.rect(screen,(0,0,0),(0,90,250,100),1)
								#更新屏幕
								pygame.display.update()	
								#卸载掉上一首音乐
								pygame.mixer.music.unload()
								#选音乐窗口
								music_path = filedialog.askopenfilename(title = "请选择音乐", filetypes = [("音乐",".mp3")])
								if music_path != "":
									music_last = music_path
									music_name = os.path.basename(music_path)
									text_music_name = font_30_size .render(("当前的音乐是:" + music_name),True,(0,0,0))
								else:
									music_path = music_last	
					#音乐开关
					if 25 <= mouse[0] <= 75 and 242 <= mouse[1] <= 267:
						#设置已打开
						if set_enter == True:
							#绘制白色按钮特效矩形
							pygame.draw.rect(screen,(255,255,255),(25,242,50,25),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#绘制黑色按钮特效矩形
							pygame.draw.rect(screen,(0,0,0),(25,242,50,25),1)
							#更新屏幕
							pygame.display.update()	
							if music_switch == True:	
								#音乐开关已关闭
								music_switch = False			
							else:
								#音乐开关已打开
								music_switch = True
					#朗读开关
					if 25 <= mouse[0] <= 75 and 332 <= mouse[1] <= 357:
						#设置已打开
						if set_enter == True:
							#绘制白色按钮特效矩形
							pygame.draw.rect(screen,(255,255,255),(25,332,50,25),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#绘制黑色按钮特效矩形
							pygame.draw.rect(screen,(0,0,0),(25,332,50,25),1)
							#更新屏幕
							pygame.display.update()
							if speak_switch == True:	
								#朗读开关已关闭
								speak_switch = False			
							else:
								#朗读开关已打开
								speak_switch = True
					#帮助
					if 0 <= mouse[0] <= 100 and 370 <= mouse[1] <= 420:
						#设置已打开
						if set_enter == True:
							#绘制白色按钮特效矩形
							pygame.draw.rect(screen,(255,255,255),(0,370,100,50),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#绘制黑色按钮特效矩形
							pygame.draw.rect(screen,(0,0,0),(0,370,100,50),1)
							#更新屏幕
							pygame.display.update()
							os.system(r"notepad 关于/帮助.txt")
					#关于
					if 0 <= mouse[0] <= 100 and 420 <= mouse[1] <= 470:
						#设置已打开
						if set_enter == True:
							#绘制白色按钮特效矩形
							pygame.draw.rect(screen,(255,255,255),(0,420,100,50),1)
							#更新屏幕
							pygame.display.update()
							#特效延迟
							time.sleep(0.1)
							#绘制黑色按钮特效矩形
							pygame.draw.rect(screen,(0,0,0),(0,420,100,50),1)
							#更新屏幕
							pygame.display.update()
							os.system(r"notepad 关于/关于.txt")
			#打开设置
			if set_enter == True:
				#设置打开时的特效
				if move_set_x != -1000:
					move_set_x -= 2
					move_set_y -= 1
				#背景X轴位置
				photo_background_x = 1000 + move_set_x
				#背景y轴位置
				photo_background_y = 500 + move_set_y
				#绘制背景
				build_background()
				#返回
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,500 + move_set_y,100,50),1)
				#绘制返回矩形
				pygame.draw.rect(screen,(185,122,87),(1001 + move_set_x,501 + move_set_y,98,48),0)
				#打印返回字体
				screen.blit(text_back,(1020 + move_set_x,507 + move_set_y))
				#选音乐
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,590 + move_set_y,250,100),1)
				#绘制选音乐矩形
				pygame.draw.rect(screen,(0,162,234),(1001 + move_set_x,591 + move_set_y,248,98),0)
				#打印选音乐字体
				screen.blit(text_choose_music,(1050 + move_set_x,610 + move_set_y))
				#帮助
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,870 + move_set_y,100,50),1)
				#绘制帮助矩形
				pygame.draw.rect(screen,(106,59,187),(1001 + move_set_x,871 + move_set_y,98,48),0)
				#打印帮助字体
				screen.blit(text_help,(1020 + move_set_x,877 + move_set_y))
				#关于
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,920 + move_set_y,100,50),1)
				#绘制关于矩形
				pygame.draw.rect(screen,(179,229,33),(1001 + move_set_x,921 + move_set_y,98,48),0)
				#打印关于字体
				screen.blit(text_about,(1020 + move_set_x,927 + move_set_y))
				#音乐开关
				#打开音乐开关时开关滑块移动的距离
				if music_switch == True and move_music_switch_x < 24:
					move_music_switch_x += 1
				#关闭音乐开关时开关滑块移动的距离	
				if music_switch == False and move_music_switch_x > 0:
					move_music_switch_x -= 1
				#黑色部分移动的距离转换
				move_music_switch_x_black = 0 - move_music_switch_x
				if music_switch == True:
					#白色部分	
					music_switch_white = pygame.Surface((move_music_switch_x,23),pygame.SRCALPHA)
					music_switch_white.fill((255,255,255,128))
					screen.blit(music_switch_white,(1026 + move_set_x,743 + move_set_y))
					#黑色部分
					music_switch_black = pygame.Surface((24 + move_music_switch_x_black,23),pygame.SRCALPHA)
					music_switch_black.fill((0,0,0,128))
					screen.blit(music_switch_black,(1050 + move_music_switch_x_black + move_set_x,743 + move_set_y))
					#音乐开关已打开
					screen.blit(text_music_switch_on,(1000 + move_set_x,695 + move_set_y))
				else:
					#白色部分
					music_switch_white = pygame.Surface((move_music_switch_x,23),pygame.SRCALPHA)
					music_switch_white.fill((255,255,255,128))
					screen.blit(music_switch_white,(1026,743))
					#黑色部分
					music_switch_black = pygame.Surface((24 + move_music_switch_x_black,23),pygame.SRCALPHA)
					music_switch_black.fill((0,0,0,128))
					screen.blit(music_switch_black,(1050 + move_music_switch_x_black + move_set_x,743 + move_set_y))
					#音乐开关已关闭
					screen.blit(text_music_switch_off,(1000 + move_set_x,695 + move_set_y))
					#状态栏阴影                     
					screen.blit(music_state,(1000 + move_set_x,550 + move_set_y))
					#选音乐阴影		                      
					screen.blit(choose_music_state,(1000 + move_set_x,590 + move_set_y))
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1025 + move_set_x,742 + move_set_y,50,25),1)
				#音乐开关滑块
				pygame.draw.rect(screen,(199,191,230),(1026 + move_music_switch_x + move_set_x,743 + move_set_y,24,23),0)
				#朗读开关
				#打开朗读开关时开关滑块移动的距离
				if speak_switch == True and move_speak_switch_x < 24:
					move_speak_switch_x += 1
				#关闭朗读开关时开关滑块移动的距离	
				if speak_switch == False and move_speak_switch_x > 0:
					move_speak_switch_x -= 1
				#黑色部分移动的距离转换
				move_speak_switch_x_black = 0 - move_speak_switch_x
				if speak_switch == True:
					#白色部分	
					speak_switch_white = pygame.Surface((move_speak_switch_x,23),pygame.SRCALPHA)
					speak_switch_white.fill((255,255,255,128))
					screen.blit(speak_switch_white,(1026 + move_set_x,833 + move_set_y))
					#黑色部分
					speak_switch_black = pygame.Surface((24 + move_speak_switch_x_black,23),pygame.SRCALPHA)
					speak_switch_black.fill((0,0,0,128))
					screen.blit(speak_switch_black,(1050 + move_speak_switch_x_black + move_set_x,833 + move_set_y))
					#朗读开关已打开
					screen.blit(text_speak_switch_on,(1000 + move_set_x,785 + move_set_y))
				else:
					#白色部分
					speak_switch_white = pygame.Surface((move_speak_switch_x,23),pygame.SRCALPHA)
					speak_switch_white.fill((255,255,255,128))
					screen.blit(speak_switch_white,(1026,743))
					#黑色部分
					speak_switch_black = pygame.Surface((24 + move_speak_switch_x_black,23),pygame.SRCALPHA)
					speak_switch_black.fill((0,0,0,128))
					screen.blit(speak_switch_black,(1050 + move_speak_switch_x_black + move_set_x,833 + move_set_y))
					#朗读开关已关闭
					screen.blit(text_speak_switch_off,(1000 + move_set_x,785 + move_set_y))
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1025 + move_set_x,832 + move_set_y,50,25),1)
				#朗读开关滑块
				pygame.draw.rect(screen,(128,128,255),(1026 + move_speak_switch_x + move_set_x,833 + move_set_y,24,23),0)
				#打印音乐文件名
				screen.blit(text_music_name,(1000 + move_set_x,555 + move_set_y))
			#关闭设置
			if set_enter == False:
				#绘制主界面按钮
				#背景X轴位置
				photo_background_x = 0
				#背景y轴位置
				photo_background_y = 0
				#绘制背景
				build_background()
				#选名单
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(0,400,250,100),1)
				#绘制选名单矩形
				pygame.draw.rect(screen,(255,201,13),(1,401,248,98),0)
				#打印选名单字体
				screen.blit(text_choose_list,(55,420))
				#三连抽
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(250,400,250,100),1)
				#绘制三连抽矩形
				pygame.draw.rect(screen,(237,27,36),(251,401,248,98),0)  
				#打印三连抽字体
				screen.blit(text_names_3,(300,420))
				#幸运单抽
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(500,400,250,100),1)
				#绘制幸运单抽矩形
				pygame.draw.rect(screen,(35,177,77),(501,401,248,98),0)
				#打印幸运单抽字体
				screen.blit(text_name,(530,420))
				#设置
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(750,400,250,100),1)
				#绘制设置矩形
				pygame.draw.rect(screen,(255,127,38),(751,401,248,98),0)
				#打印设置字体
				screen.blit(text_set,(820,420))
				if speak_switch == True:
					#朗读开关已打开
					screen.blit(text_speak_switch_on,(850,365))
				else:
					#朗读开关已关闭
					screen.blit(text_speak_switch_off,(850,365))
				if music_switch == True:
					#打印音乐文件名
					screen.blit(text_music_name,(0,325))
				else:
					#打印音乐文件名
					screen.blit(text_music_name,(0,325))
					#状态栏阴影                       
					screen.blit(music_state,(0,320))
				if list_already == True:
					#打印名单文件名
					screen.blit(text_names_list,(0,365))	
				else:
					#警告
					screen.blit(warn_list,(375,145))
				#设置关闭时的特效
				if move_set_x != 0:
					move_set_x += 2
					move_set_y += 1
				#背景X轴位置
				photo_background_x = 1000 + move_set_x
				#背景y轴位置
				photo_background_y = 500 + move_set_y
				#绘制背景
				build_background()
				#返回
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,500 + move_set_y,100,50),1)
				#绘制返回矩形
				pygame.draw.rect(screen,(185,122,87),(1001 + move_set_x,501 + move_set_y,98,48),0)
				#打印返回字体
				screen.blit(text_back,(1020 + move_set_x,507 + move_set_y))
				#选音乐
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,590 + move_set_y,250,100),1)
				#绘制选音乐矩形
				pygame.draw.rect(screen,(0,162,234),(1001 + move_set_x,591 + move_set_y,248,98),0)
				#打印选音乐字体
				screen.blit(text_choose_music,(1050 + move_set_x,610 + move_set_y))
				#帮助
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,870 + move_set_y,100,50),1)
				#绘制帮助矩形
				pygame.draw.rect(screen,(106,59,187),(1001 + move_set_x,871 + move_set_y,98,48),0)
				#打印帮助字体
				screen.blit(text_help,(1020 + move_set_x,877 + move_set_y))
				#关于
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1000 + move_set_x,920 + move_set_y,100,50),1)
				#绘制关于矩形
				pygame.draw.rect(screen,(179,229,33),(1001 + move_set_x,921 + move_set_y,98,48),0)
				#打印关于字体
				screen.blit(text_about,(1020 + move_set_x,927 + move_set_y))
				#音乐开关
				#打开音乐开关时开关滑块移动的距离
				if music_switch == True and move_music_switch_x < 24:
					move_music_switch_x += 1
				#关闭音乐开关时开关滑块移动的距离	
				if music_switch == False and move_music_switch_x > 0:
					move_music_switch_x -= 1
				#黑色部分移动的距离转换
				move_music_switch_x_black = 0 - move_music_switch_x
				if music_switch == True:
					#白色部分	
					music_switch_white = pygame.Surface((move_music_switch_x,23),pygame.SRCALPHA)
					music_switch_white.fill((255,255,255,128))
					screen.blit(music_switch_white,(1026 + move_set_x,743 + move_set_y))
					#黑色部分
					music_switch_black = pygame.Surface((24 + move_music_switch_x_black,23),pygame.SRCALPHA)
					music_switch_black.fill((0,0,0,128))
					screen.blit(music_switch_black,(1050 + move_music_switch_x_black + move_set_x,743 + move_set_y))
					#音乐开关已打开
					screen.blit(text_music_switch_on,(1000 + move_set_x,695 + move_set_y))
				else:
					#白色部分
					music_switch_white = pygame.Surface((move_music_switch_x,23),pygame.SRCALPHA)
					music_switch_white.fill((255,255,255,128))
					screen.blit(music_switch_white,(1026,743))
					#黑色部分
					music_switch_black = pygame.Surface((24 + move_music_switch_x_black,23),pygame.SRCALPHA)
					music_switch_black.fill((0,0,0,128))
					screen.blit(music_switch_black,(1050 + move_music_switch_x_black + move_set_x,743 + move_set_y))
					#音乐开关已关闭
					screen.blit(text_music_switch_off,(1000 + move_set_x,695 + move_set_y))
					#状态栏阴影                     
					screen.blit(music_state,(1000 + move_set_x,550 + move_set_y))
					#选音乐阴影		                      
					screen.blit(choose_music_state,(1000 + move_set_x,590 + move_set_y))
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1025 + move_set_x,742 + move_set_y,50,25),1)
				#音乐开关滑块
				pygame.draw.rect(screen,(199,191,230),(1026 + move_music_switch_x + move_set_x,743 + move_set_y,24,23),0)
				#朗读开关
				#打开朗读开关时开关滑块移动的距离
				if speak_switch == True and move_speak_switch_x < 24:
					move_speak_switch_x += 1
				#关闭朗读开关时开关滑块移动的距离	
				if speak_switch == False and move_speak_switch_x > 0:
					move_speak_switch_x -= 1
				#黑色部分移动的距离转换
				move_speak_switch_x_black = 0 - move_speak_switch_x
				if speak_switch == True:
					#白色部分	
					speak_switch_white = pygame.Surface((move_speak_switch_x,23),pygame.SRCALPHA)
					speak_switch_white.fill((255,255,255,128))
					screen.blit(speak_switch_white,(1026 + move_set_x,833 + move_set_y))
					#黑色部分
					speak_switch_black = pygame.Surface((24 + move_speak_switch_x_black,23),pygame.SRCALPHA)
					speak_switch_black.fill((0,0,0,128))
					screen.blit(speak_switch_black,(1050 + move_speak_switch_x_black + move_set_x,833 + move_set_y))
					#朗读开关已打开
					screen.blit(text_speak_switch_on,(1000 + move_set_x,785 + move_set_y))
				else:
					#白色部分
					speak_switch_white = pygame.Surface((move_speak_switch_x,23),pygame.SRCALPHA)
					speak_switch_white.fill((255,255,255,128))
					screen.blit(speak_switch_white,(1026,743))
					#黑色部分
					speak_switch_black = pygame.Surface((24 + move_speak_switch_x_black,23),pygame.SRCALPHA)
					speak_switch_black.fill((0,0,0,128))
					screen.blit(speak_switch_black,(1050 + move_speak_switch_x_black + move_set_x,833 + move_set_y))
					#朗读开关已关闭
					screen.blit(text_speak_switch_off,(1000 + move_set_x,785 + move_set_y))
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(1025 + move_set_x,832 + move_set_y,50,25),1)
				#朗读开关滑块
				pygame.draw.rect(screen,(128,128,255),(1026 + move_speak_switch_x + move_set_x,833 + move_set_y,24,23),0)
				#打印音乐文件名
				screen.blit(text_music_name,(1000 + move_set_x,555 + move_set_y))
			#三连抽
			#快速三连抽
			if names_3_fast_switch == True and names_3_switch == False:
				#绘制白色按钮特效矩形
				pygame.draw.rect(screen,(255,255,255),(250,400,250,100),1)
				with open(names_list_utf_8,encoding = "utf-8",errors = "replace") as names_list:
					names_lines = names_list.readlines()
					#第1个人
					names_3_fast_1 = choice(names_lines)																				
					#第2个人
					names_3_fast_2 = choice(names_lines)
					#第3个人
					names_3_fast_3 = choice(names_lines)
					#第1个人的姓名去除"\n"
					names_3_fast_1 = re.sub(r"\n","",names_3_fast_1)
					#第2个人的姓名去除"\n"
					names_3_fast_2 = re.sub(r"\n","",names_3_fast_2)
					#第3个人的姓名去除"\n"
					names_3_fast_3 = re.sub(r"\n","",names_3_fast_3)
					text_lucky_names_3_fast_1 = font_50_size.render((names_3_fast_1),True,(0,0,255))							
					text_lucky_names_3_fast_2 = font_50_size.render((names_3_fast_2),True,(0,0,255))
					text_lucky_names_3_fast_3 = font_50_size.render((names_3_fast_3),True,(0,0,255))
					#打印第1个人的姓名					
					screen.blit(text_lucky_names_3_fast_1,(130,145))
					#打印第2个人的姓名					
					screen.blit(text_lucky_names_3_fast_2,(430,145))
					#打印第3个人的姓名					
					screen.blit(text_lucky_names_3_fast_3,(730,145))
			#真正的三连抽
			if names_3_switch == True:
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(250,400,250,100),1)
				while True:
					with open(names_list_utf_8,encoding = "utf-8",errors = "replace") as names_list:
						names_lines = names_list.readlines()
						#第1个人
						names_3_1 = choice(names_lines)																				
						#第2个人
						names_3_2 = choice(names_lines)
						#第3个人
						names_3_3 = choice(names_lines)
						#第1个人的姓名去除"\n"
						names_3_1 = re.sub(r"\n","",names_3_1)
						#第2个人的姓名去除"\n"
						names_3_2 = re.sub(r"\n","",names_3_2)
						#第3个人的姓名去除"\n"
						names_3_3 = re.sub(r"\n","",names_3_3)
						#防止同时出现的3个相同的名字
						if names_3_1 == names_3_2 or names_3_1 == names_3_3 or names_3_2 == names_3_3:
							continue
						#防重复列表
						#人员名单长度
						names_lines_max = len(names_lines)
						#检测人员名单是否是3的倍数
						while True:
							if names_lines_max % 3 == 0:	
								names_lines_max_3 = names_lines_max
								break
							else:
								names_lines_max -= 1 
								continue
						#第1个人的姓名是否在防重复列表中
						if names_3_1 in pass_names_3:	
							continue
						#第2个人的姓名是否在防重复列表中
						if names_3_2 in pass_names_3:	
							continue
						#第3个人的姓名是否在防重复列表中
						if names_3_3 in pass_names_3:	
							continue
						#抽中的第1个人的姓名加入防重复列表
						pass_names_3.append(names_3_1)
						#抽中的第2个人的姓名加入防重复列表
						pass_names_3.append(names_3_2)
						#抽中的第3个人的姓名加入防重复列表
						pass_names_3.append(names_3_3) 
						#防重复列表长度
						pass_names_max = len(pass_names_3)
						if pass_names_max == names_lines_max_3:
							pass_names_3.clear()
						text_lucky_names_3_1 = font_50_size.render((names_3_1),True,(0,0,255))							
						text_lucky_names_3_2 = font_50_size.render((names_3_2),True,(0,0,255))
						text_lucky_names_3_3 = font_50_size.render((names_3_3),True,(0,0,255))
						#三连抽已完成
						names_3_already = True
						#开始朗读
						speak_start = True
						break		
			#三连抽姓名打印及朗读
			if names_3_already == True and set_enter == False:
				#打印第1个人的姓名					
				screen.blit(text_lucky_names_3_1,(130,145))
				if speak_start == True:
					#更新屏幕
					pygame.display.update()
					if speak_switch == True:
						#朗读第1个人的姓名
						pyttsx3.speak(names_3_1)
				#打印第2个人的姓名						
				screen.blit(text_lucky_names_3_2,(430,145))
				if speak_start == True:
					#更新屏幕
					pygame.display.update()
					if speak_switch == True:
						#朗读第2个人的姓名
						pyttsx3.speak(names_3_2)
				#打印第3个人的姓名					
				screen.blit(text_lucky_names_3_3,(730,145))
				if speak_start == True:
					#更新屏幕
					pygame.display.update()
					if speak_switch == True:
						#朗读第3个人的姓名
						pyttsx3.speak(names_3_3)
					#关闭三连抽
					names_3_switch = False
					#停止朗读
					speak_start = False
			#幸运单抽
			#快速幸运单抽
			if name_fast_switch == True and name_switch == False:
				#绘制白色按钮特效矩形
				pygame.draw.rect(screen,(255,255,255),(500,400,250,100),1)
				with open(names_list_utf_8,encoding = "utf-8",errors = "replace") as names_list:
					names_lines = names_list.readlines()
					#幸运儿
					name_fast = choice(names_lines)					
					#幸运儿的姓名去除"\n"
					name_fast = re.sub(r"\n","",name_fast)			
					text_lucky_name_fast = font_50_size.render((name_fast),True,(0,0,255))							
					#打印幸运儿的姓名					
					screen.blit(text_lucky_name_fast,(430,145))	
			#真正的幸运单抽
			if name_switch == True:
				#绘制黑色按钮特效矩形
				pygame.draw.rect(screen,(0,0,0),(500,400,250,100),1)
				while True:
					with open(names_list_utf_8,encoding = "utf-8",errors = "replace") as names_list:
						names_lines = names_list.readlines()
						#幸运儿
						name = choice(names_lines)									
						#幸运儿的姓名去除"\n"
						name = re.sub(r"\n","",name)
						#防重复列表
						#人员名单长度
						names_lines_max = len(names_lines)
						#幸运儿的姓名是否在防重复列表中
						if name in pass_names:	
							continue					
						#幸运儿的姓名加入防重复列表
						pass_names.append(name)					 
						#防重复列表长度
						pass_names_max = len(pass_names)
						if pass_names_max == names_lines_max:
							pass_names.clear()						
						text_lucky_name = font_50_size.render((name),True,(0,0,255))							
						#幸运单抽已完成
						name_already = True
						#开始朗读
						speak_start = True
						break					
			#幸运单抽姓名打印及朗读
			if name_already == True and set_enter == False:
				#打印幸运儿的姓名					
				screen.blit(text_lucky_name,(430,145))
				if speak_start == True:
					#更新屏幕
					pygame.display.update()
					if speak_switch == True:
						#朗读幸运儿的姓名
						pyttsx3.speak(name)
					#关闭幸运单抽
					name_switch = False
					#停止朗读
					speak_start = False
			#更新屏幕
			pygame.display.update()