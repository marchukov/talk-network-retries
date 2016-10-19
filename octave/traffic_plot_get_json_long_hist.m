RJ = csvread('~/tmp/pyconcz2016-net-failures/naive_get_json_long.csv');

% Request times
RJT = RJ(:,2);
RJTP = RJT(RJT <= prctile(RJT, 95))

set(gcf,'PaperUnits','inches','PaperSize',[15,5],'PaperPosition',[0 0 15 5]);

hist(RJTP, 'facecolor', [0,0.75,1], 'edgecolor', 'none');
title('95% Percentile Request Distribution');
xlabel('Time (sec)');
grid();

% print -dpng -r100 file.png
% convert file.png -trim file.png
