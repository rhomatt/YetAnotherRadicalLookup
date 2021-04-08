// Temporary announcements
import React from 'react';
import {Typography} from '@material-ui/core';

export default function About(){
	return (
		<Typography>
			This is a Japanese -> English (and for now, only that way) lookup site that allows the use of special wildcards
			<br/>
			Use ? as a basic wildcard character, or * for 0 to any amount of characters.
			<br/>
			<br/>

			This site also allows for groupings of parts within parenthesis. For instance:
			<br/>

			日?(言五)
			<br/>

			will search for all words that start with 日, any following character, and ending with a character with both 言 and 五 in it
		</Typography>
		);
}
