iter=10

sum_score=0
win_cnt=0
for ((i = 0; i < iter; i++)); do
	if ((i % 10 == 0)); then
		echo iter: $i
	fi
	score=$(/c/Python27/python.exe pacman.py -p ReflexAgent -l openClassic -q | grep "Average Score" | sed 's/.*: //' | sed 's/\..*//')
	# score=$(/c/Python27/python.exe pacman.py -p ReflexAgent -l testClassic -q | grep "Average Score" | sed 's/.*: //' | sed 's/\..*//')
	# echo $score
	if ((score > 0)); then
		win_cnt=$((win_cnt+1))
	fi
	sum_score=$((sum_score + score))
done
echo ""
echo Total Iter: $iter
echo win count: $win_cnt
echo Average Score: $((sum_score / iter))
