data <- read.csv(file = "data/edit_counts_total.csv", header = TRUE, row.names = 1)

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

sample <- cbind(data$X2017, label_wmc, label_zh_hans)

colnames(sample) <- c("Total", "Membership", "zh_hans")

model <- lm(Total ~ Membership, data = sample)

summary(model)

model <- lm(Total ~ zh_hans, data = sample)

summary(model)

model <- lm(Total ~ Membership + zh_hans, data = sample)

summary(model)

data <- read.csv(file = "data/edit_counts_main.csv", header = TRUE, row.names = 1)

sample <- cbind(data$X2017, label_wmc, label_zh_hans)

colnames(sample) <- c("Main", "Membership", "zh_hans")

model <- lm(Main ~ Membership, data = sample)

summary(model)

model <- lm(Main ~ zh_hans, data = sample)

summary(model)

model <- lm(Main ~ Membership + zh_hans, data = sample)

summary(model)

data <- read.csv(file = "data/edit_counts_wikipedia.csv", header = TRUE, row.names = 1)

sample <- cbind(data$X2017, label_wmc, label_zh_hans)

colnames(sample) <- c("Wikipedia", "Membership", "zh_hans")

model <- lm(Wikipedia ~ Membership, data = sample)

summary(model)

model <- lm(Wikipedia ~ zh_hans, data = sample)

summary(model)

model <- lm(Wikipedia ~ Membership + zh_hans, data = sample)

summary(model)
