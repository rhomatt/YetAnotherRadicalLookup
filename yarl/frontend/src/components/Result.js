import React from 'react';
import { Card, CardContent, Typography } from '@material-ui/core/';

export default class Result extends React.Component{
	constructor(props){
		super(props);
		this.word = props.word
	}

	render(){
		return (
			<Card>
				<CardContent>
					<Typography variant="h4">
						{this.word}
					</Typography>
				</CardContent>
			</Card>
		);
	}
}
