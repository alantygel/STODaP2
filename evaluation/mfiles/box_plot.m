close all; clear all;
% //task : water, budget, proc
% //method: ex, sto, free

files = {'results', 'results_notnull','results_correct'}

for i=1:3

	close all
	eval(files{i})
	h = figure(1);
	boxplot(tct_sm,1);
	set (gca, 'XTick', [1 2 3]) 
	set (gca, 'XTickLabel', {'Exversion', 'STODaP', 'Free'}) 

	xlabel ('Search Method')
	ylabel ('seconds')
	% legend(h,,'location','Northwest')
	grid
	W = 4; H = 3;
	set(h,'PaperUnits','inches')
	set(h,'PaperOrientation','portrait');
	set(h,'PaperSize',[H,W])
	set(h,'PaperPosition',[0,0,W,H])

	FN = findall(h,'-property','FontName');
	set(FN,'FontName','/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf');
	FS = findall(h,'-property','FontSize');
	set(FS,'FontSize',8);

	print(h,'-dpng','-color',['~/Dropbox/Alan - Doutorado/Tese Text/tese/images/tct_boxplot'  files{i}  '.png'])
end

