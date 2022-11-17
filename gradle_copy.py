# -*- coding:utf-8 -*-

"""
python版本： 3.7
将gradle下载的缓存拷贝到指定的输出目录。
-src=~/.gradle
-dst=xxx
"""

import os
import shutil
import argparse


def copy_jar_package(src, dst):
    # dirname is md5?
    for root, dirs, files in os.walk(src):
        for f in files:
            filename = os.path.join(root, f)
            # md5目录下就是文件，不存在多个路径，否则会异常
            outname = os.path.join(dst, f)
            print("[copy] {0} to {1}".format(filename, outname))
            shutil.copy(filename, outname)


def gradle_copy_impl(src, dst):
    # like tracker/26.4.3 tracker/27.0.1
    for dirname in os.listdir(src):
        src_name = os.path.join(src, dirname)
        dst_name = os.path.join(dst, dirname)
        for version_name in os.listdir(src_name):
            out_version_name = os.path.join(dst_name, version_name)
            if not os.path.exists(out_version_name):
                os.makedirs(out_version_name)
            copy_jar_package(os.path.join(src_name, version_name), out_version_name)


def copy_package_impl(src, dst):
    # like 'com.android' 'com.android.tools.build'
    for package_name in os.listdir(src):
        split_path = package_name.replace('.', '/')
        out_path = os.path.join(dst, split_path)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        gradle_copy_impl(os.path.join(src, package_name), out_path)


def main():
    parse = argparse.ArgumentParser(prog="GradleCopy")
    # 如果可以拿到用戶目录，就用用户目录拼  get home path
    user_path = os.environ.get("HOME")
    if user_path:
        # 没有检查路径是否存在  not check the path is exist.
        gradle_path = os.path.join(user_path, ".gradle")
        parse.add_argument("-src", help=".gradle root path", type=str, default=gradle_path)
    else:
        parse.add_argument("-src", help=".gradle root path", type=str)
    parse.add_argument("-dst", help="copy to dst path", type=str)
    arguments = parse.parse_args()
    assert arguments.src and os.path.exists(arguments.src), "{0} path is not found!".format(arguments.src)
    assert arguments.dst and os.path.exists(arguments.dst), "{0} path is not found!".format(arguments.dst)
    gradle_cache_path = os.path.join(arguments.src, "caches/modules-2/files-2.1")
    assert os.path.exists(gradle_cache_path), "gradle not cache?!"
    # 执行拷贝 copy... no safe.
    copy_package_impl(gradle_cache_path, arguments.dst)


if __name__ == '__main__':
    main()


