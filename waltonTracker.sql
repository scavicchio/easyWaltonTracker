CREATE TABLE BlockChain(
	blockNum INT,
	miner VARCHAR,
	extra_data VARCHAR,
	difficulty INT,
	timest TIMESTAMP,

	PRIMARY KEY (blockNum)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Miner(
	miner VARCHAR,
	balance DECIMAL,
	totalBlocksMined INT,
	masternode BOOLEAN,
	guardian BOOLEAN,

	PRIMARY KEY (miner)
)   ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE Block(
	blockNum INT,
	miner VARCHAR,
	reward DECIMAL,
	difficulty INT,

	PRIMARY KEY (blockNum) REFERENCES BlockChain(blockNum)
	FOREIGN KEY (miner) REFERENCES BlockChain(miner)
)	ENGINE=InnoDB DEFAULT CHARSET=latin1;

