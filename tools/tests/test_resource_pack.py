# CHANGELOG v1.0 · 2026-09-27 — 승인·해시·버전·경로·독립 사용 회귀 검사
"""최종본 등록에서 미승인·변경 파일이 섞이지 않는지 검사합니다."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

spec=importlib.util.spec_from_file_location('resource_pack',Path(__file__).resolve().parents[1]/'resource_pack.py')
rp=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rp)


class Registration(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.project=self.root/'projects/pixelart-icon'
        (self.project/'export').mkdir(parents=True)
        (self.project/'releases').mkdir()
        (self.project/'pixelart-icon-modules.json').write_text('{"on":[]}')
        (self.root/'resources').mkdir()
        rp.write_json(self.root/'resources/manifest.json',{'schema_version':1,'assets':[]})
        self.png=self.project/'export/icon.png'
        im=Image.new('RGBA',(32,32),(0,0,0,0))
        im.putpixel((15,15),(60,100,160,255))
        im.save(self.png)
        self.plan={'schema_version':1,'project':'pixelart-icon','id':'icons.items.test-gem','version':'v1','kind':'icon',
                   'default_file':'icon.png','files':[{'source':'export/icon.png','name':'icon.png','role':'icon','size':[32,32],'sha256':rp.digest(self.png.read_bytes())}],
                   'approval':{'status':'approved','by':'테스트 사용자','at':'2026-09-27','evidence':'격리된 시험용 승인'},
                   'review':{'status':'passed','by':'테스트','at':'2026-09-27','evidence':'격리된 시험용 검수','checks':{'visual':True,'project_spec':True,'rights':True}}}
        self.path=self.project/'releases/test.json'
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        rp.write_json(self.path,self.plan)

    def test_dry_run_writes_nothing(self):
        rp.publish(self.root,self.path)
        self.assertEqual(list((self.root/'resources').iterdir()),[self.root/'resources/manifest.json'])

    def test_publish_copy_and_overwrite(self):
        rp.publish(self.root,self.path,True)
        self.assertEqual(rp.check(self.root/'resources')['등록_버전'],1)
        isolated=self.root/'standalone'
        shutil.copytree(self.root/'resources',isolated)
        self.assertEqual(rp.check(isolated)['등록_버전'],1)
        with self.assertRaises(ValueError): rp.publish(self.root,self.path,True)
        self.plan['version']='v2'; self.save()
        rp.publish(self.root,self.path,True)
        self.assertEqual(rp.check(self.root/'resources')['등록_버전'],2)

    def test_unapproved_and_incomplete_review(self):
        self.plan['approval']['status']='pending'; self.save()
        with self.assertRaises(ValueError): rp.publish(self.root,self.path,True)
        self.plan['approval']['status']='approved'
        self.plan['review']['checks'].pop('rights'); self.save()
        with self.assertRaises(ValueError): rp.publish(self.root,self.path,True)

    def test_stale_hash(self):
        self.png.write_bytes(self.png.read_bytes()+b'changed')
        with self.assertRaises(ValueError): rp.publish(self.root,self.path,True)

    def test_bad_size_and_black(self):
        self.plan['files'][0]['size']=[16,16]; self.save()
        with self.assertRaises(ValueError): rp.publish(self.root,self.path)
        im=Image.open(self.png).convert('RGBA'); im.putpixel((1,1),(0,0,0,255)); im.save(self.png)
        self.plan['files'][0].update(size=[32,32],sha256=rp.digest(self.png.read_bytes())); self.save()
        with self.assertRaises(ValueError): rp.publish(self.root,self.path)

    def test_escape_and_reserved_names(self):
        for source in ['../../outside.png','C:/outside.png','export/../icon.png']:
            self.plan['files'][0]['source']=source; self.save()
            with self.assertRaises(ValueError): rp.publish(self.root,self.path)
        self.plan['files'][0]['source']='export/icon.png'
        self.plan['id']='icons...escape'; self.save()
        with self.assertRaises(ValueError): rp.publish(self.root,self.path)

    def test_source_symlink_escape(self):
        outside=self.root/'outside'; outside.mkdir()
        shutil.copyfile(self.png,outside/'icon.png')
        link=self.project/'export/link'
        try: link.symlink_to(outside,target_is_directory=True)
        except OSError: self.skipTest('환경에서 심볼릭 링크 생성 불가')
        self.plan['files'][0]['source']='export/link/icon.png'; self.save()
        with self.assertRaises(ValueError): rp.publish(self.root,self.path)

    def test_manifest_failure_rolls_back_new_version(self):
        with patch.object(rp.os,'replace',side_effect=OSError('시험용 실패')):
            with self.assertRaises(OSError): rp.publish(self.root,self.path,True)
        self.assertFalse((self.root/'resources/icons/items/test-gem/v1').exists())
        self.assertEqual(rp.check(self.root/'resources')['등록_버전'],0)

    def test_file_tamper_detected(self):
        rp.publish(self.root,self.path,True)
        png=self.root/'resources/icons/items/test-gem/v1/icon.png'
        png.write_bytes(png.read_bytes()+b'changed')
        with self.assertRaises(ValueError): rp.check(self.root/'resources')

    def test_animation_bounds_and_timing(self):
        files={'walk.png':{'role':'sheet','size':[64,32]}}
        a={'walk':{'file':'walk.png','frame_size':[32,32],'loop':True,'frames':[{'rect':[32,0,32,32],'duration_ms':100}]}}
        rp.verify_animation(a,files)
        a['walk']['frames'][0]['rect'][0]=33
        with self.assertRaises(ValueError): rp.verify_animation(a,files)
        a['walk']['frames'][0].update(rect=[32,0,32,32],duration_ms=0)
        with self.assertRaises(ValueError): rp.verify_animation(a,files)


if __name__=='__main__':
    unittest.main()
