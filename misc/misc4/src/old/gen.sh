#RANDOM=drawtext='fontsize=30:fontfile=FreeSerif.ttf:fontcolor=white:text='"'GHIDRA Training'"':x=if(eq(mod(t\,5)\,0)\,rand(0\,(w-text_w))\,x):y=if(eq(mod(t\,5)\,0)\,rand(0\,(h-text_h))\,y)'

FLAG="flag{l34kfr33_n4tion4l_s3cur1ty}"
LOGO=drawtext='fontsize=22:fontfile=FreeSerif.ttf:fontcolor=white:text='"'GHIDRA Training'"':x=(w-text_w)/2-10:y=h-40:enable=lt(t\,8)'
NSA_LOGO="movie=watermarklogo.png [wow]"

FLAG1=drawtext='fontsize=20:fontfile=DejaVuSansMono.ttf:fontcolor=white:x=100:y=x/dar:enable=lt(mod(t\,3)\,1):text='"'FLAG(1/4):'"
LONG=drawtext='fontsize=15:fontfile=DejaVuSansMono:fontcolor=white:text='"'TOP SECRET//CYBER//NOFORN'"':y=h-line_h:x=-50*mod(t\,180)+300'

CREDITS=drawtext='fontsize=20:fontfile=FreeSerif.ttf:line_spacing=5:fontcolor=white:textfile=test.txt:y=h-20*(t-12):x=10'

#ffmpeg -y -f lavfi -i color=color=black -vf "$TEST" -t 180 black_long.mp4
#ffmpeg -y -f lavfi -i color=color=black -vf "$LOGO,$TEST,$LONG" -t 180 black_long.mp4
./ffmpeg-git-20190320-amd64-static/ffmpeg -y -f lavfi -i color=color=black -vf "movie=watermarklogo.png,scale=180:180 [logo]; [in][logo] overlay=(W-w)/2-10:(H-h)/2-20, fade=in:0:25, fade=out:200:25, $LONG, $LOGO,$CREDITS [out]" -t 3600 black_long.mp4

