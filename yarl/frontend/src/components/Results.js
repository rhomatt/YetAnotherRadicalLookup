import React from 'react';
import { List, ListItem, ListItemText, ListSubheader, Grid } from '@material-ui/core/';
import Result from './Result';

export default class Results extends React.Component{
	constructor(props){
		super(props);
		this.getResults = props.getResults
	}

	render(){
		return <List component="nav">
					<ListSubheader>Results</ListSubheader>
					{this.getResults().map(res => (
						<ListItem>
							<Result word={res}/>
						</ListItem>
						)
					)}
				</List>
	}
}
