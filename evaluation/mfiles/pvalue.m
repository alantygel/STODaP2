clear('all');
correlations;

printf('\t')
for i=1:9
	printf ('%i\t',i)
end
	printf('\n')
for i=1:9
	printf ('%i\t',i)
	for j=1:9
		if (i != j) && (i!=2) && (j!=2)
			x = anova(vars{i},vars{j});
		else
			x = 1;
		end
		printf ('%.4f\t',x)
		% printf ('%i-%i',i,j)
	end
	printf('\n')
end