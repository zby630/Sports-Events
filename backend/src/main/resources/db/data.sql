-- 初始化数据脚本
-- 校园体育赛事管理系统

-- 强制客户端使用 utf8mb4，避免中文被按 latin1 解析导致乱码
SET NAMES utf8mb4;

-- 清空表数据（按外键依赖顺序）
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE result;
TRUNCATE TABLE schedule;
TRUNCATE TABLE registration;
TRUNCATE TABLE sport_item;
TRUNCATE TABLE event;
TRUNCATE TABLE news;
TRUNCATE TABLE sys_user;
SET FOREIGN_KEY_CHECKS = 1;

-- 插入用户数据
-- 密码都是 123456 (BCrypt加密)
INSERT INTO sys_user (username, password, real_name, gender, role, student_no, department, class_name, phone, email, status) VALUES
('admin', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '系统管理员', 1, 'ADMIN', 'A001', '体育部', NULL, '13800000001', 'admin@school.edu.cn', 1),
('teacher1', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '张教练', 1, 'TEACHER', 'T001', '体育部', NULL, '13800000002', 'teacher1@school.edu.cn', 1),
('teacher2', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '李裁判', 2, 'TEACHER', 'T002', '体育部', NULL, '13800000003', 'teacher2@school.edu.cn', 1),
('student1', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '王小明', 1, 'STUDENT', '2021001', '计算机学院', '软件2101', '13800000011', 'student1@school.edu.cn', 1),
('student2', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '李小红', 2, 'STUDENT', '2021002', '计算机学院', '软件2101', '13800000012', 'student2@school.edu.cn', 1),
('student3', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '张小强', 1, 'STUDENT', '2021003', '机械学院', '机械2101', '13800000013', 'student3@school.edu.cn', 1),
('student4', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '刘小芳', 2, 'STUDENT', '2021004', '经济学院', '金融2101', '13800000014', 'student4@school.edu.cn', 1),
('student5', '$2b$10$9K20PaabaIQvn5uD95DxvOXy.o8b92t1J4e87MnILSd9bImD12OS.', '陈小伟', 1, 'STUDENT', '2021005', '外语学院', '英语2101', '13800000015', 'student5@school.edu.cn', 1);

-- 插入赛事数据 (状态: 1-草稿 2-报名中 3-进行中 4-已结束)
INSERT INTO event (event_name, event_type, description, start_date, end_date, reg_start_date, reg_end_date, location, organizer, contact_phone, status, create_by) VALUES
('2024年春季田径运动会', 'TRACK_FIELD', '一年一度的春季田径运动会，展现青春活力，挑战自我极限！', '2024-04-15', '2024-04-17', '2024-03-01', '2024-04-10', '校田径场', '体育部', '0571-88888888', 2, 1),
('2024年篮球联赛', 'BALL', '校园篮球联赛，以球会友，展现团队精神！', '2024-05-01', '2024-05-30', '2024-04-01', '2024-04-25', '体育馆', '体育部', '0571-88888889', 2, 1),
('2024年游泳比赛', 'SWIMMING', '夏日清凉，泳池竞技！', '2024-06-10', '2024-06-12', '2024-05-15', '2024-06-05', '游泳馆', '体育部', '0571-88888890', 1, 1),
('2023年秋季运动会', 'TRACK_FIELD', '2023年秋季综合运动会', '2023-10-20', '2023-10-22', '2023-09-15', '2023-10-15', '校田径场', '体育部', '0571-88888888', 4, 1),
('2026年冬季运动会', 'TRACK_FIELD', '面向全校师生的冬季田径运动会，当前开放报名。', '2026-12-05', '2026-12-06', '2026-11-01', '2026-12-04', '校田径场', '体育部', '0571-88888888', 2, 1);

-- 插入运动项目数据 (性别限制: 0-不限 1-男 2-女)
INSERT INTO sport_item (event_id, item_name, item_type, gender_limit, max_participants, current_participants, rules, result_type, result_unit, status) VALUES
-- 春季田径运动会项目
(1, '男子100米', 'TRACK', 1, 30, 5, '预赛取前8名进入决赛', 'TIME', '秒', 1),
(1, '女子100米', 'TRACK', 2, 30, 3, '预赛取前8名进入决赛', 'TIME', '秒', 1),
(1, '男子跳远', 'FIELD', 1, 20, 4, '每人3次试跳，取最好成绩', 'DISTANCE', '米', 1),
(1, '女子跳远', 'FIELD', 2, 20, 2, '每人3次试跳，取最好成绩', 'DISTANCE', '米', 1),
(1, '男子铅球', 'FIELD', 1, 15, 3, '每人3次投掷，取最好成绩', 'DISTANCE', '米', 1),
-- 篮球联赛项目
(2, '男子篮球', 'BALL', 1, 120, 0, '5人制，小组赛+淘汰赛', 'SCORE', '分', 1),
(2, '女子篮球', 'BALL', 2, 80, 0, '5人制，小组赛+淘汰赛', 'SCORE', '分', 1),
-- 游泳比赛项目
(3, '男子50米自由泳', 'WATER', 1, 20, 0, '预赛取前8名进入决赛', 'TIME', '秒', 1),
(3, '女子50米自由泳', 'WATER', 2, 20, 0, '预赛取前8名进入决赛', 'TIME', '秒', 1),
-- 2026年冬季运动会项目（当前可报名）
(5, '男子100米', 'TRACK', 1, 30, 0, '预赛取前8名进入决赛', 'TIME', '秒', 1),
(5, '女子100米', 'TRACK', 2, 30, 0, '预赛取前8名进入决赛', 'TIME', '秒', 1),
(5, '男子跳远', 'FIELD', 1, 20, 0, '每人3次试跳，取最好成绩', 'DISTANCE', '米', 1),
(5, '女子跳远', 'FIELD', 2, 20, 0, '每人3次试跳，取最好成绩', 'DISTANCE', '米', 1);

-- 插入报名数据 (状态: 1-待审核 2-已通过 3-已拒绝 4-已取消)
INSERT INTO registration (event_id, sport_item_id, user_id, status, remark) VALUES
(1, 1, 4, 2, '希望能取得好成绩'),
(1, 1, 6, 2, NULL),
(1, 3, 4, 2, NULL),
(1, 3, 6, 1, '第一次参加'),
(1, 2, 5, 2, NULL),
(1, 4, 5, 2, NULL),
(1, 5, 4, 2, NULL),
(1, 1, 8, 2, NULL),
(1, 3, 8, 2, NULL);

-- 插入赛程数据 (状态: 1-未开始 2-进行中 3-已结束)
INSERT INTO schedule (event_id, sport_item_id, schedule_name, round_no, group_no, match_date, start_time, end_time, location, status, remark) VALUES
(1, 1, '预赛', 1, '1', '2024-04-15', '09:00', '10:00', '田径场1号跑道', 1, '男子100米预赛第1组'),
(1, 1, '预赛', 2, '2', '2024-04-15', '10:00', '11:00', '田径场1号跑道', 1, '男子100米预赛第2组'),
(1, 1, '决赛', 3, '1', '2024-04-16', '15:00', '16:00', '田径场1号跑道', 1, '男子100米决赛'),
(1, 2, '预赛', 1, '1', '2024-04-15', '09:30', '10:30', '田径场2号跑道', 1, '女子100米预赛'),
(1, 2, '决赛', 2, '1', '2024-04-16', '15:30', '16:30', '田径场2号跑道', 1, '女子100米决赛'),
(1, 3, '决赛', 1, '1', '2024-04-17', '09:00', '12:00', '跳远沙坑', 1, '男子跳远决赛');

-- 插入新闻/公告数据 (状态: 0-草稿 1-已发布)
INSERT INTO news (title, content, news_type, event_id, view_count, is_top, publish_time, status, create_by) VALUES
('2024年春季田径运动会报名开始', '各位同学，2024年春季田径运动会报名已经开始，请有意参加的同学尽快报名！报名截止日期为4月10日。', 'NOTICE', 1, 156, 1, '2024-03-01 09:00:00', 1, 1),
('篮球联赛即将开赛', '2024年校园篮球联赛将于5月1日正式开赛，欢迎各学院组队参加！', 'NEWS', 2, 89, 0, '2024-04-01 10:00:00', 1, 1),
('运动会安全须知', '为确保运动会顺利进行，请所有参赛选手和观众遵守以下安全规定...', 'NOTICE', 1, 234, 1, '2024-04-10 14:00:00', 1, 1),
('上届运动会精彩回顾', '2023年秋季运动会圆满落幕，让我们一起回顾那些精彩瞬间...', 'NEWS', 4, 567, 0, '2023-10-25 16:00:00', 1, 1);

-- 插入历史成绩数据（2023年秋季运动会）
INSERT INTO result (event_id, sport_item_id, user_id, score, score_unit, ranking, points, is_record, recorder_id, remark) VALUES
(4, 1, 4, 11.25, '秒', 1, 10, 0, 2, '表现优秀'),
(4, 1, 6, 11.58, '秒', 2, 8, 0, 2, NULL),
(4, 1, 8, 11.89, '秒', 3, 6, 0, 2, NULL);
