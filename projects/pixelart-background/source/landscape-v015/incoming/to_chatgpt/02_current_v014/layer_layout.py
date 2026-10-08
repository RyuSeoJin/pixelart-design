# CHANGELOG v5.1 · 2026-10-08 — 숲 바닥도 공통 4단위 규격을 적용합니다.
# CHANGELOG v5.0 · 2026-10-08 — 그림 한 칸 = PNG 1픽셀 · PNG 1픽셀 = 월드 4단위(RecordTales 고정 규격). 화면 크기는 v4.0과 같습니다.
# CHANGELOG v4.0 · 2026-10-08 — 1픽셀=1월드단위와 상단 확장 레이어입니다.
"""모든 월드 레이어를 같은 기준점과 배율로 화면에 투영합니다.

UE에 자동 적용되지 않는 배치 기준입니다. 고정 월드 크기를 먼저 등록한 다음,
건물·캐릭터에도 world_to_screen과 같은 카메라 변환을 적용합니다.
"""
from math import ceil, floor, isfinite

PARALLAX = {'sky':(0,1), 'stars':(0,1), 'clouds_high':(1,20), 'clouds':(1,20),
            'mountains_far':(1,10), 'mountains_near':(1,5),
            'trees_back':(3,10), 'buildings':(2,5), 'window_lights':(2,5),
            'trees_front':(1,2), 'street_tile':(1,1), 'lower_base':(0,1)}
PIVOT = (960, 832)
BACKGROUND_ORIGIN = (0, 0)
UPPER_SKY_ORIGIN = (0, -2496)
MAXIMUM_VIEW_WORLD_RECT = (-2880, -2496, 7680, 4320)


UNITS_PER_TEXEL = 4   # PNG 1픽셀 = 월드 4단위(그림 한 칸 = PNG 1픽셀로 저장 — 화면 크기는 4배로 그린다)


def world_geometry(layer, texture_size):
    """PNG 1픽셀을 월드 4단위로 배치합니다(manifest world_rect와 같아야 합니다).

    하늘·별·높은 구름은 월드y=-2496에서 시작합니다(하늘·별 높이 3576, 높은 구름 2496).
    나머지 배경은 원점(0,0)이며 그림의 지면(PNG y=208)이 월드y=832와 일치합니다.
    바닥 타일은 PNG 120×30 = 월드 480×120이며 윗변이 월드y=832입니다.
    """
    width, height = texture_size
    if layer == 'lower_base':
        return (0, 0, 1920, 1080)          # 화면 고정 색면 — 화면 1920×1080 기준
    w, h = width * UNITS_PER_TEXEL, height * UNITS_PER_TEXEL
    if layer == 'street_tile':
        return (0, 832, w, h)
    x, y = UPPER_SKY_ORIGIN if layer in ('sky','stars','clouds_high') else BACKGROUND_ORIGIN
    return (x, y, w, h)


def world_to_screen(point, zoom, camera_x=0, parallax=(1,1), viewport=(1920,1080)):
    """월드 좌표를 공통 카메라 변환으로 화면에 투영합니다."""
    if not isfinite(zoom) or not .25 <= zoom <= 1:
        raise ValueError('지원 배율은1/4~1입니다.')
    if not isfinite(camera_x) or min(viewport) <= 0 or abs(viewport[0]*9-viewport[1]*16)>16:
        raise ValueError('유효한 카메라와16:9 내부 뷰포트가 필요합니다.')
    u=viewport[1]/1080
    n,d=parallax
    # 이동 비율만 다릅니다. 확대 중심과 zoom은 모든 월드에 공통입니다.
    return ((PIVOT[0]+(point[0]-PIVOT[0]-camera_x*n/d)*zoom)*u,
            (PIVOT[1]+(point[1]-PIVOT[1])*zoom)*u)


def rectangles(layer, texture_size, zoom, camera_x=0, viewport=(1920,1080)):
    """전체 스프라이트의 화면 x,y,폭,높이를 반환합니다.

    RTStageSprites::Place를 쓰면 하단 중앙은(x+w/2,y+h)입니다.
    lower_base는 월드가 아니라 하단 UI용 화면 색면입니다.
    """
    if layer=='lower_base':
        world_to_screen(PIVOT,zoom,camera_x,viewport=viewport)
        return [(0,0,*viewport)]
    x,y,w,h=world_geometry(layer,texture_size)
    left,top=world_to_screen((x,y),zoom,camera_x,PARALLAX[layer],viewport)
    _,bottom=world_to_screen((x,y+h),zoom,camera_x,PARALLAX[layer],viewport)
    period=w*zoom*viewport[1]/1080
    offset=left%period
    rnd=lambda v: floor(v+.5)
    y0,y1=rnd(top),rnd(bottom)
    result=[]
    for i in range(-1,ceil(viewport[0]/period)+1):
        # 공통 경계를 반올림하므로 소수 배율에서도 타일 사이 틈이 없습니다.
        x0,x1=rnd(offset+i*period),rnd(offset+(i+1)*period)
        if x1>0 and x0<viewport[0]: result.append((x0,y0,x1-x0,y1-y0))
    return result
