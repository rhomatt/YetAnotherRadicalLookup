import React from 'react';
import { List, ListItem, ListItemText, ListSubheader, Grid } from '@material-ui/core/';
import Result from './Result';

export default class Results extends React.Component{
	constructor(props){
		super(props);
	}

	render(){
		const results = this.props.results;
		console.log("from results: " + results)
		return <List component="nav">
					<ListSubheader>Results</ListSubheader>
					{results.map(res => (
						<ListItem key={res.id}>
							<Result result={res}/>
						</ListItem>
						)
					)}
				</List>
	}
}
