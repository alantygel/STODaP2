close all; clear all;
% //task : water, budget, proc
% //method: ex, sto, free

task = {'\textbf{Exversion}', '\textbf{STODaP}', '\textbf{Free}'};

results;

printf('>>> TCT\n')
printf ('\\textbf{Tasks / Search Methods} & \\textbf{Water Quality} & 	\\textbf{Budget information} ')
printf  (' &	\\textbf{Procurement} &	\\textbf{Average and Standard Deviation} ')
printf (' & \\textbf{Accepted Answers (\\%%)} \\\\ \\hline \n')
for i=1:3
	printf('%s & ', task{i})
	for j=1:3
		printf ('%.2f &',mean(tct{(i-1)*3+j}))
	end
	printf('%.2f & ', mean([tct{(i-1)*3+1} tct{(i-1)*3+2} tct{(i-1)*3+3}]))
	printf('%.2f \\\\ \\hline \n', mean([accept{(i-1)*3+1} accept{(i-1)*3+2} accept{(i-1)*3+3}]))
end
printf('\\textbf{Average} & ')
for i=0:2
	printf('%.2f & ', mean([tct{1+i} tct{4+i} tct{7+i}]))
end
printf(' & \\\\ \\hline \n')
printf('\\textbf{Acceptance} & ')
for i=0:2
	printf('%.2f & ', mean([accept{1+i} accept{4+i} accept{7+i}]))
end
printf(' & \\\\ \\hline')


printf('\n\n>>> ACCEPTANCE RATE\n')

printf ('\\textbf{Tasks / Search Methods} & \\textbf{Water Quality} & 	\\textbf{Budget information} ')
printf  (' &	\\textbf{Procurement} &	\\textbf{Average and Standard Deviation} ')
printf (' & \\textbf{TCT (s)} \\\\ \\hline \n')
for i=1:3
	printf('%s & ', task{i})
	for j=1:3
		printf ('%.2f &',mean(accept{(i-1)*3+j}))
	end
	printf('%.2f &', mean([accept{(i-1)*3+1} accept{(i-1)*3+2} accept{(i-1)*3+3}]))
	printf('%.2f \\\\ \\hline \n', mean([tct{(i-1)*3+1} tct{(i-1)*3+2} tct{(i-1)*3+3}]))

end
printf('\\textbf{Acceptance} & ')
for i=0:2
	printf('%.2f & ', mean([accept{1+i} accept{4+i} accept{7+i}]))
end

printf(' & \\\\ \\hline \n')
printf('\\textbf{TCT} & ')
for i=0:2
	printf('%.2f & ', mean([tct{1+i} tct{4+i} tct{7+i}]))
end
printf(' & \\\\ \\hline\n')
% for i=1:9
% 	printf ('%.2f \t %.2f \t %i \n',mean(a{i}), std(a{i}), length(a{i}))
% end
