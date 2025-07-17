from flask import Flask, render_template, jsonify
import psutil
import os
import logging
from datetime import datetime
import pytz
import math

# 配置日志时区为北京时间
logging.Formatter.converter = lambda *args: datetime.now(pytz.timezone('Asia/Shanghai')).timetuple()

app = Flask(__name__)

# 添加自定义过滤器用于格式化文件大小
@app.template_filter('format_size')
def format_size(bytes):
    if bytes == 0:
        return '0 Bytes'
    k = 1024
    sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    i = int(math.floor(math.log(bytes, k)))
    return f"{round(bytes / math.pow(k, i), 2)} {sizes[i]}"

@app.route('/')
def index():
    # 获取系统磁盘分区信息
    partitions = []
    for part in psutil.disk_partitions():
        try:
            # 跳过CD-ROM和空设备
            if 'cdrom' in part.opts or part.fstype == '':
                continue
            # 获取分区使用情况
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                'device': part.device,
                'mountpoint': part.mountpoint,
                'fstype': part.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        except PermissionError:
            # 跳过无权限访问的分区
            continue
        except OSError:
            # 处理其他可能的错误
            continue
    return render_template('index.html', partitions=partitions)

@app.route('/api/partitions')
def api_partitions():
    """
    API接口：获取所有磁盘分区信息
    """
    partitions = []
    for part in psutil.disk_partitions():
        try:
            if 'cdrom' in part.opts or part.fstype == '':
                continue
            usage = psutil.disk_usage(part.mountpoint)
            partitions.append({
                'device': part.device,
                'mountpoint': part.mountpoint,
                'fstype': part.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent
            })
        except PermissionError:
            continue
        except OSError:
            continue
    return jsonify(partitions)

@app.route('/api/disk_usage/<path:mountpoint>')
def api_disk_usage(mountpoint):
    """
    API接口：获取指定挂载点的磁盘使用情况
    :param mountpoint: 磁盘挂载点路径
    """
    try:
        usage = psutil.disk_usage(mountpoint)
        return jsonify({
            'total': usage.total,
            'used': usage.used,
            'free': usage.free,
            'percent': usage.percent
        })
    except PermissionError:
        return jsonify({'error': '没有权限访问此分区'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/directory_list/<path:mountpoint>')
def api_directory_list(mountpoint):
    """
    API接口：获取指定挂载点下的目录列表及大小
    :param mountpoint: 磁盘挂载点路径
    """
    try:
        directories = []
        # 获取目录列表（排除系统保护目录）
        for entry in os.scandir(mountpoint):
            if entry.is_dir(follow_symlinks=False) and not entry.name.startswith('.'):
                try:
                    size = 0
                    file_count = 0
                    for dirpath, dirnames, filenames in os.walk(entry.path):
                        for f in filenames:
                            fp = os.path.join(dirpath, f)
                            try:
                                size += os.path.getsize(fp)
                                file_count += 1
                            except (OSError, PermissionError):
                                continue
                    directories.append({
                        'name': entry.name,
                        'path': entry.path,
                        'size': size,
                        'file_count': file_count
                    })
                except (PermissionError, OSError):
                    continue
        # 按目录大小排序（降序）
        directories.sort(key=lambda x: x['size'], reverse=True)
        return jsonify(directories)
    except PermissionError:
        return jsonify({'error': '没有权限访问此目录'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 创建必要的目录
    if not os.path.exists('static'):
        os.makedirs('static')
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 启动Flask应用
    app.run(debug=True, host='127.0.0.1', port=5000)
