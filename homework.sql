/*
 Navicat Premium Data Transfer

 Source Server         : homework
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : homework

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 08/12/2023 14:30:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comeandpay
-- ----------------------------
DROP TABLE IF EXISTS `comeandpay`;
CREATE TABLE `comeandpay`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `entryformID` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `isPayed` enum('是','否') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '否',
  `isCome` enum('是','否') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '否',
  `courseID` int NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for companyapply
-- ----------------------------
DROP TABLE IF EXISTS `companyapply`;
CREATE TABLE `companyapply`  (
  `companyApplyID` int NOT NULL AUTO_INCREMENT COMMENT '公司申请ID',
  `companyName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司名称',
  `field` enum('前端','后端','数据库','服务器','人工智能','区块链') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '需要培训的领域',
  `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公司的通讯邮件地址',
  `state` enum('未处理','已同意') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '未处理' COMMENT '申请的状态',
  `applyTime` datetime(0) NOT NULL COMMENT '申请发送的时间',
  PRIMARY KEY (`companyApplyID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `courseID` int NOT NULL AUTO_INCREMENT COMMENT '课程ID',
  `executorID` int NOT NULL COMMENT '执行人ID',
  `teacherID` int NOT NULL COMMENT '教师ID',
  `companyApplyID` int NOT NULL COMMENT '公司培训申请ID',
  `courseName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课程名称',
  `courseContent` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课程内容',
  `field` enum('前端','后端','数据库','服务器','人工智能','区块链') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课程方向',
  `startTime` date NOT NULL COMMENT '开始时间',
  `endTime` date NOT NULL COMMENT '结束时间',
  `coursePlace` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '开课地点',
  `free` int NOT NULL COMMENT '培训费用',
  `courseState` enum('schedule','pending','1') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'schedule' COMMENT '课程状态',
  PRIMARY KEY (`courseID`) USING BTREE,
  INDEX `course_teacherID`(`teacherID`) USING BTREE,
  INDEX `course_executor`(`executorID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for entryform
-- ----------------------------
DROP TABLE IF EXISTS `entryform`;
CREATE TABLE `entryform`  (
  `entryformID` int NOT NULL AUTO_INCREMENT,
  `courseID` int NOT NULL,
  `isCompany` enum('是','否') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `studentName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `studentSex` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `studentCompany` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `studentField` enum('前端','后端','数据库','服务器','人工智能','区块链') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `studentLevel` enum('优秀','良好','中等','一般') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `studentEmail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `entryformState` enum('已报名','同意报名','拒绝报名') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '已报名',
  PRIMARY KEY (`entryformID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for executor
-- ----------------------------
DROP TABLE IF EXISTS `executor`;
CREATE TABLE `executor`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执行人的用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执行人的密码',
  `executorName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执行人姓名',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for manager
-- ----------------------------
DROP TABLE IF EXISTS `manager`;
CREATE TABLE `manager`  (
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '经理的用户名',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '经理的密码',
  PRIMARY KEY (`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for questionnaire
-- ----------------------------
DROP TABLE IF EXISTS `questionnaire`;
CREATE TABLE `questionnaire`  (
  `questionnaireID` int NOT NULL AUTO_INCREMENT COMMENT '调查表ID',
  `courseID` int NOT NULL COMMENT '课程ID',
  `teacherScore` int NOT NULL COMMENT '教师评分',
  `courseScore` int NOT NULL COMMENT '课程评分',
  `executorScore` int NOT NULL COMMENT '执行人评分',
  `comment` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '课程评论与建议',
  PRIMARY KEY (`questionnaireID`) USING BTREE,
  INDEX `questionnaire_courseID`(`courseID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for summary
-- ----------------------------
DROP TABLE IF EXISTS `summary`;
CREATE TABLE `summary`  (
  `summaryID` int NOT NULL AUTO_INCREMENT COMMENT '汇总表ID',
  `courseID` int NOT NULL COMMENT '课程ID',
  `teacherScore` float(255, 2) NOT NULL COMMENT '教师得分',
  `courseScore` float(255, 2) NOT NULL COMMENT '课程得分',
  `executorScore` float(255, 2) NOT NULL COMMENT '执行人得分',
  `totalStudent` int NOT NULL COMMENT '参加的人数',
  `money` int NOT NULL COMMENT '总金额',
  PRIMARY KEY (`summaryID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for teacher
-- ----------------------------
DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher`  (
  `teacherID` int NOT NULL AUTO_INCREMENT COMMENT '教师ID',
  `teacherName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '教师姓名',
  `teacherTitle` enum('教授','副教授','讲师') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '教师职称',
  `teacherField` enum('前端','后端','数据库','服务器','人工智能','区块链','') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '' COMMENT '教师领域',
  `teacherEmail` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '教师的邮件地址',
  `teacherPhone` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT '0' COMMENT '教师电话',
  PRIMARY KEY (`teacherID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
