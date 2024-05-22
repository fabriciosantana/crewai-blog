import streamlit as st

cols   = st.columns(2)
fields = ["id", "content"]

# header
for col, field in zip(cols, fields):
	col.write("**"+field+"**")

# rows
for idx, row in zip([1,2,3],["test1", "test2", "test3"]):
	
	col1, col2 = st.columns(2)
	col1.write(str(idx))
	
	placeholder = col2.empty()
	show_more   = placeholder.button("more", key=idx, type="primary")

	# if button pressed
	if show_more:

		# rename button
		placeholder.button("less", key=str(idx)+"_")
		
		# do stuff
		st.write("This is some more stuff with a checkbox")
		temp = st.selectbox("Select one", ["A", "B", "C"])
		st.write("You picked ", temp)
		st.write("---")