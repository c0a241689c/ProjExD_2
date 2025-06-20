import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA={ #　移動量辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect)->tuple[bool,bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：縦横方向の画面内外判定結果
    画面内ならTrue, 画面外ならFalse
    """

    yoko,tate=True,True #初期値：画面の中
    if rct.left <0 or WIDTH < rct.right:
        yoko=False
    if rct.top <0 or HEIGHT < rct.bottom:
        tate=False
    return yoko, tate #縦横方向の画面内判定結果を返す
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0))
    bb_rct=bb_img.get_rect()
    bb_rct.centerx=random.randint(0,WIDTH) #横座標用の乱数
    bb_rct.centery=random.randint(0,HEIGHT) #縦座標用の乱数
    vx, vy = +5, +5  # 爆弾の移動速度


    def gmover(screen:pg.surface):     
        enn= pg.Surface((WIDTH,HEIGHT))
        fonto = pg.font.Font(None, 80)
        txt = fonto.render("Game Over",True,(255,0,0))
        txt_rct=txt.get_rect()
        rightgm_img=pg.image.load("fig/8.png")
        leftgm_img=pg.image.load("fig/8.png")
        rightgm_rct=rightgm_img.get_rect()
        leftgm_rct=leftgm_img.get_rect()
        txt_rct.center=550,300
        rightgm_rct.center=350,300
        leftgm_rct.center=750,300
        screen.fill((0,0,0))
        screen.set_alpha(128)
        screen.blit(rightgm_img,rightgm_rct)
        screen.blit(leftgm_img,leftgm_rct)
        screen.blit(txt,txt_rct)
        pg.display.update()
        time.sleep(5)

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            gmover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, delta in DELTA.items():
            if key_lst[key]:
                sum_mv[0] +=delta[0]
                sum_mv[1] +=delta[1]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1]) #移動をなかったことにする
        
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx,vy)
        yoko, tate=check_bound(bb_rct)
        if not yoko:
            vx*= -1
        if not tate:
            vy*= -1
        screen.blit(bb_img, bb_rct) #爆弾の描画
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
