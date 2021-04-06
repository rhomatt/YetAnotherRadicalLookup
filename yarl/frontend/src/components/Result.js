import React from 'react';
import { Card, CardContent, Typography } from '@material-ui/core/';

export default class Result extends React.Component{
	constructor(props){
		super(props);
		this.result = props.result
	}

	render(){
		return (
			<Card>
				<CardContent>
					<Typography variant="h4">
						{this.result.readings}
					</Typography>
					<Typography variant="h4">
						{this.result.definitions}
					</Typography>
				</CardContent>
			</Card>
		);
	}
}
