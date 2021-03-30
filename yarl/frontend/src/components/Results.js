import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import Grid from '@material-ui/core/Grid';

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
							<ListItemText primary={res}/>
						</ListItem>
						)
					)}
				</List>
	}
}
