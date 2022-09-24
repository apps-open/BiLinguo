from enum import Enum

class Action(Enum):
	CREATE_VOCABULARY = 0
	LOAD_VOCABULARY = 1
	MANAGE_VOCABULARY = 2
	ADD_WORD = 3
	EDIT_WORD = 4
	TEST = 5