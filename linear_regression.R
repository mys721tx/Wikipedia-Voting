data <- read.csv(file = "edit_counts.csv", header = TRUE, row.names = 1)

label_wmc <- read.csv(
	file = "wmc_memberships.csv",
	header = TRUE,
	row.names = 1,
	stringsAsFactors=FALSE,
	colClasses = c("character", "logical")
)

label_zh_hans <- read.csv(
	file = "simplified_chinese_users.csv",
	header = TRUE,
	row.names = 1,
	stringsAsFactors=FALSE,
	colClasses = c("character", "logical")
)

sample <- cbind(data$X2017, label_wmc, label_zh_hans)

colnames(sample) <- c("Counts", "Membership", "zh_hans")

model <- lm(Counts ~ Membership, data = sample)

summary(model)

model <- lm(Counts ~ zh_hans, data = sample)

summary(model)

model <- lm(Counts ~ Membership + zh_hans, data = sample)

summary(model)
