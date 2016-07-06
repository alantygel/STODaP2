close all
results;
h = figure(1);

accept{10} = [accept{1} accept{2} accept{3}];
accept{11} = [accept{4} accept{5} accept{6}];
accept{12} = [accept{7} accept{8} accept{9}];

t = {'Exversion', 'STODaP', 'Free','Aggregated'}
for i=1:4
	subplot(2,2,i)
	s = (i-1)*3 + 1;
	boxplot(accept(s:s+2),1);
	title (t(i))
	set (gca, 'XTick', [1 2 3]) 
	set (gca, 'XTickLabel', {'Q1', 'Q2', 'Q3'}) 
	axis ([0.4 3.6 30 100])
	grid
	ylabel ('Precision (%)')
end
set (gca, 'XTickLabel', {'Exversion', 'STODaP', 'Free'}) 


	% legend(h,,'location','Northwest')
	
	W = 6; H = 3;

	FN = findall(h,'-property','FontName');
	set(FN,'FontName','/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf');
	FS = findall(h,'-property','FontSize');
	set(FS,'FontSize',8);

	set(h,'PaperUnits','inches')
	set(h,'PaperOrientation','portrait');
	set(h,'PaperSize',[H,W])
	set(h,'PaperPosition',[0,0,W,H])



	print(h,'-dpng',['~/Dropbox/Alan - Doutorado/Tese Text/tese/images/precision_boxplot.png'])
