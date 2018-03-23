require(rms)

data <- read.csv(file = "pca_result.csv", header = TRUE, row.names = 1)
label <- read.csv(file = "wmc_memberships.csv", header = TRUE, row.names = 1)

levels(label$Membership) <- c(0, 1)

sample <- cbind(data, label)

model <- lrm(Membership ~ PC1 + PC2, data = sample)

model
