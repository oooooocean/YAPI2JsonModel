struct JsonModel: Decodable {
	/// 口腔专家二诊业务单id
	let oralDiagnosisId: Int
	let userId: Int
	/// 阡陌专家二诊业务单id
	let qianmoDiagnosisId: Int
	/// 口腔医生id
	let oralDoctorId: Int
	/// 阡陌医生id
	let qianmoDoctorId: Int
	/// 医生姓名
	let doctorName: String
	/// 专家二诊服务编号
	let serviceNo: String
	/// 二诊状态
	/// 0 :初始化1 :待支付2 :待审核3 :待补充4 :审核已拒诊5 :专家已拒诊6 :审核已通过7 :报告已完成8 :已追问，待回复9 :追问回复已完成；患者未追问直接结束订单；追问倒计时已结束自动完成订单10 :已取消
	let diagnosisStatus: Int
	/// 审核通过时间
	let checkPassTime: String
	/// 报告生成时间
	let reportTime: String
	/// 病历提交时间
	let medicalRecordCommitTime: String
	/// 患者病历
	let medicalRecord: MedicalRecord
	/// 诊断结果
	let diagnosisResult: DiagnosisResult
	/// 剩余追问时间
	let leftTime: Int
}

struct DiagnosisResult: Decodable {
	/// 病情资料解读
	let medicalRecordExplanation: String
	/// 病情建议
	let diseaseAdvice: String
	/// 护理建议
	let nursingAdvice: String
	/// 饮食建议
	let dietaryAdvice: String
	/// 就医指导
	let medicalGuidance: String
	/// 医师签名
	let doctorSignatureUrl: String
	/// 提交报告日期
	let reportDate: String
	/// 患者追问
	let appendQuestionContent: String
	/// 专家回复
	let reply: String
}

struct MedicalRecord: Decodable {
	/// 就诊人姓名
	let realname: String
	/// 就诊人性别(0男，1女，2保密)
	let gender: Int
	/// 就诊人年龄
	let age: Int
	/// 患病时长
	let diseaseDuration: String
	/// 病情描述
	let diseaseDescription: String
	/// 疾病症状标签
	let expertSecondDiagnosisTags: String
	/// 是否药物过敏
	let drugAllergy: Bool
	/// 药物过敏信息
	let drugAllergyInfo: String
	/// 是否有正在使用的药物
	let drugInuse: Bool
	/// 正在使用的药物信息
	let drugInuseInfo: String
	/// 正在使用的药物图片url（多个图片的url用英文逗号分割）
	let drugInuseUrl: String
	/// 当前是否怀孕
	let pregnant: Bool
	/// 预产期
	let expectedDateOfChildbirth: String
}

struct JsonModel: Decodable {
	/// 口腔医生id
	let oralDoctorId: Int
	/// 阡陌医生id
	let qianmoDoctorId: Int
	/// 医生名称
	let hospitalDoctorName: String
	/// 头像
	let headUrl: String
	/// 性别
	let sex: String
	/// 年龄
	let age: Int
	/// 擅长
	let goodat: String
	/// 医院名称
	let communityHospitalName: String
	/// 科室名称
	let departmentName: String
	/// 教育职称
	let educationTitle: String
	/// 职称
	let jobName: String
	/// 医生简介
	let doctorDesc: String
	/// 科研著作
	let scientifiResearch: String
	/// 论文著作
	let paper: String
	/// 服务人数
	let serviceCnt: Int
	/// 二诊费用原价
	let originalPrice: Double
	/// 划线价
	let counterPrice: Double
	/// 成果荣誉
	let contribution: String
	/// 任职
	let position: String
}