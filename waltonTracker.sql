CREATE TABLE BlockChain(
	blockNum INT,
	miner VARCHAR,
	extra_data VARCHAR,
	difficulty INT,
	timest TIMESTAMP,

	PRIMARY KEY (blockNum)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;