require(rms)

data <- read.csv(file = "data/pca_result.csv", header = TRUE, row.names = 1)

label_wmc <- read.csv(
	file = "data/wmc_memberships.csv",
	header = TRUE,
	row.names = 1,
	stringsAsFactors=FALSE,
	colClasses = c("character", "logical")
)

label_zh_hans <- read.csv(
	file = "data/simplified_chinese_users.csv",
	header = TRUE,
	row.names = 1,
	stringsAsFactors=FALSE,
	colClasses = c("character", "logical")
)

sample <- cbind(data, label_wmc, label_zh_hans)

model <- lrm(Membership ~ PC1 + PC2, data = sample)

model

model <- lrm(zh_hans ~ PC1 + PC2, data = sample)

model

sample <- cbind(
	data[which(!label_wmc$Membership),],
	label_zh_hans[!label_wmc$Membership,]
)

colnames(sample) <- c("PC1", "PC2", "zh_hans")

model <- lrm(zh_hans ~ PC1 + PC2, data = sample)

model
