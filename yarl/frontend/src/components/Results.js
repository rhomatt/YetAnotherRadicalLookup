import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import Grid from '@material-ui/core/Grid';

export default class Results extends React.Component{
	constructor(props){
		super(props);
	}

	render(){
		return <List component="nav">
					<ListSubheader>Results</ListSubheader>
					{this.props.results.map(res => (
						<ListItem>
							<ListItemText primary={res} align="center"/>
						</ListItem>
						)
					)}
				</List>
	}
}
