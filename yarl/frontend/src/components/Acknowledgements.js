import React from 'react';
import {Typography} from '@material-ui/core';

export default function Acknowledgements(){
	return (
		<Typography>
			Acknowledgements:
			<br/>
			This package uses the RADKFILE/KRADFILE dictionary files, and can be found here: https://www.edrdg.org/krad/kradinf.html.
			<br/>
			These files are the property of the Electronic Dictionary Research and Development Group, and are used in conformance with the Group's licence, which can be found here: https://www.edrdg.org/edrdg/licence.html.
		</Typography>
		);
}

