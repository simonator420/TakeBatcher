CONTAINER TakeBatcherDialog
{
	NAME TakeBatcher;
	INCLUDE Odialog.res;
	
	LAYOUT
	{
		GroupBegin {ID=1000; ALIGN_LEFT; LAYOUT_FILL_X|LAYOUT_FILL_TOP; COLUMNS=2;}
		{
			StaticText {ID=1001; ALIGN_LEFT; NAME="General resource path"; }
			EditText {ID=1002; ALIGN_LEFT; INITW=200; }
			Button {ID=1003; ALIGN_LEFT; NAME="...";}
		}
		GroupEnd;
		
		GroupBegin {ID=1004; ALIGN_LEFT; LAYOUT_FILL_X|LAYOUT_FILL_TOP; COLUMNS=2;}
		{
			StaticText {ID=1005; ALIGN_LEFT; NAME="Relative resource path"; }
			EditText {ID=1006; ALIGN_LEFT; INITW=200; }
			Button {ID=1007; ALIGN_LEFT; NAME="...";}
		}
		GroupEnd;
		
		GroupBegin {ID=1008; ALIGN_LEFT; LAYOUT_FILL_TOP; COLUMNS=1;}
		{
			Checkbox {ID=1009; ALIGN_LEFT; NAME="Corona render multipass";}
		}
		GroupEnd;
		
		Button {ID=1010; ALIGN_CENTER_H; LAYOUT_FILL_X|LAYOUT_FILL_BOTTOM; NAME="Create takes for selected materials"; }
	}
}